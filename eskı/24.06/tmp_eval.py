import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score, f1_score, confusion_matrix

# load data

df_normal = pd.read_csv('normal_traffic.csv')
df_attack = pd.read_csv('attack_traffic.csv')
df_normal['Label'] = 0
df_attack['Label'] = 1
df_normal['Traffic_Source'] = 'normal'
df_attack['Traffic_Source'] = 'attack'
df_raw = pd.concat([df_normal, df_attack], ignore_index=True)

# recreate preprocessing from notebook
import re
PROTOCOL_PORT_MAP = {
    'TLSV1.2': 443, 'TLSV1.3': 443, 'QUIC': 443,
    'HTTP': 80, 'DNS': 53, 'SSH': 22, 'RDP': 3389,
    'LLMNR': 5355, 'SSDP': 1900, 'NTP': 123,
    'STUN': 3478, 'NBNS': 137, 'DHCP': 67,
    'NAT-PMP': 5351, 'ICMP': -1, 'ICMPV6': -1,
    'TCP': -2, 'UDP': -2,
}

def extract_dest_port(row):
    match = re.search(r'>\s*(\d+)', str(row['Info']))
    if match:
        return int(match.group(1))
    return PROTOCOL_PORT_MAP.get(str(row['Protocol']).upper(), -3)

df_raw['Dst_Port'] = df_raw.apply(extract_dest_port, axis=1)

# load threat intel
if Path('service-names-port-numbers.csv').exists():
    df_iana = pd.read_csv('service-names-port-numbers.csv', low_memory=False)
    def calculate_threat_score(text):
        if pd.isna(text):
            return 30.0
        text = str(text).lower()
        if 'ssh' in text or 'telnet' in text or 'radmin' in text or 'ms-sql' in text or 'microsoft-ds' in text:
            return 90.0
        if 'http' in text or 'web' in text or 'dns' in text:
            return 60.0
        if 'ntp' in text or 'time' in text:
            return 40.0
        return 30.0
    df_iana = df_iana.rename(columns={c: c.strip() for c in df_iana.columns})
    if 'Port Number' in df_iana.columns and 'Service Name' in df_iana.columns:
        df_iana['Dst_Port'] = pd.to_numeric(df_iana['Port Number'], errors='coerce').fillna(-1).astype(int)
        df_iana['Risk_Score'] = df_iana['Service Name'].apply(calculate_threat_score)
        df_threat_intel = df_iana[['Dst_Port', 'Service Name', 'Risk_Score']].drop_duplicates(subset=['Dst_Port'])
        df = pd.merge(df_raw, df_threat_intel, on='Dst_Port', how='left')
    else:
        df = df_raw.copy()
else:
    df = df_raw.copy()
    df['Risk_Score'] = 30.0

# engineering
if 'Risk_Score' in df.columns:
    df['Is_High_Risk'] = (df['Risk_Score'] >= 80).astype(int)
else:
    df['Is_High_Risk'] = 0

df = df.sort_values(['Source', 'Time']).reset_index(drop=True)
df['Time_Diff'] = df.groupby('Source')['Time'].diff().fillna(0)
df['Bytes_Per_Sec'] = np.where(df['Time_Diff'] > 0.005, df['Length'] / df['Time_Diff'], 0.0)
cap_value = df['Bytes_Per_Sec'].quantile(0.99)
df['Bytes_Per_Sec'] = df['Bytes_Per_Sec'].clip(upper=cap_value)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['Protocol_Enc'] = le.fit_transform(df['Protocol'].astype(str))

def port_category(port):
    if pd.isna(port) or port < 0: return 0
    if port < 1024: return 1
    if port < 49152: return 2
    return 3

df['Port_Category'] = df['Dst_Port'].apply(port_category)
FEATURES = ['Length', 'Dst_Port', 'Risk_Score', 'Is_High_Risk', 'Time_Diff', 'Bytes_Per_Sec', 'Protocol_Enc', 'Port_Category']
FEATURES = [f for f in FEATURES if f in df.columns]

X = df[FEATURES]
y = df['Label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
train_data = pd.concat([X_train, y_train], axis=1)
attack_train = train_data[train_data['Label'] == 1]
normal_train = train_data[train_data['Label'] == 0]
normal_downsampled = normal_train.sample(n=len(attack_train) * 2, random_state=42)
balanced_train = pd.concat([attack_train, normal_downsampled]).sample(frac=1, random_state=42)
X_train_bal = balanced_train.drop('Label', axis=1)
y_train_bal = balanced_train['Label']
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_bal)
X_test_scaled = scaler.transform(X_test)
rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
rf_model.fit(X_train_scaled, y_train_bal)
rf_pred = rf_model.predict(X_test_scaled)
rf_f1 = f1_score(y_test, rf_pred)
xgb_model = XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42, use_label_encoder=False, eval_metric='logloss')
xgb_model.fit(X_train_scaled, y_train_bal)
xgb_pred = xgb_model.predict(X_test_scaled)
xgb_f1 = f1_score(y_test, xgb_pred)
if xgb_f1 >= rf_f1:
    winner = 'XGBoost'
    model = xgb_model
else:
    winner = 'RandomForest'
    model = rf_model
print('rf_f1', rf_f1)
print('xgb_f1', xgb_f1)
print('winner', winner)

# final metrics
mpred = model.predict(X_test_scaled)
pprob = model.predict_proba(X_test_scaled)[:,1]
print(classification_report(y_test, mpred, target_names=['Normal (0)', 'Saldýrý (1)']))
print('auc', roc_auc_score(y_test, pprob))
cm = confusion_matrix(y_test, mpred)
print('cm', cm)
