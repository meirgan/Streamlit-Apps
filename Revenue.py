import streamlit as st
import pandas as pd

st.set_page_config(page_title="מחשבון השקעות", page_icon="💰")

st.title("💰 מחשבון השקעות עם גרף תשואה")
st.write("הכנס נתונים כדי לראות איך ההשקעה שלך צומחת לאורך הזמן.")

# --- קלט מהמשתמש ---
col1, col2 = st.columns(2)

with col1:
    initial_investment = st.number_input(
        "השקעה ראשונית (₪)",
        min_value=0.0,
        value=10000.0,
        step=1000.0
    )

    monthly_deposit = st.number_input(
        "הפקדה חודשית (₪)",
        min_value=0.0,
        value=1000.0,
        step=100.0
    )

with col2:
    annual_return_percent = st.number_input(
        "תשואה שנתית ממוצעת (%)",
        min_value=-100.0,
        value=7.0,
        step=0.5
    )

    months = st.number_input(
        "משך ההשקעה (בחודשים)",
        min_value=1,
        value=120,
        step=1
    )

# --- חישוב תשואה ---
# המרה לתשואה חודשית (ריבית דריבית)
annual_return = annual_return_percent / 100.0
monthly_return = (1 + annual_return) ** (1 / 12) - 1

balances = []
deposits_total = []
months_list = []

current_balance = initial_investment
total_deposits = initial_investment  # נחשב השקעה ראשונית כחלק מהסכום שהופקד

# חודש 0 - רק ההשקעה הראשונית
months_list.append(0)
balances.append(current_balance)
deposits_total.append(total_deposits)

for m in range(1, months + 1):
    # צמיחה חודשית + הפקדה בסוף החודש
    current_balance = current_balance * (1 + monthly_return) + monthly_deposit
    total_deposits += monthly_deposit

    months_list.append(m)
    balances.append(current_balance)
    deposits_total.append(total_deposits)

# טבלת נתונים
df = pd.DataFrame({
    "חודשים": months_list,
    "שווי תיק (₪)": balances,
    "סך הפקדות (₪)": deposits_total
}).set_index("חודשים")

st.subheader("📈 גרף צמיחת ההשקעה")
st.line_chart(df[["שווי תיק (₪)", "סך הפקדות (₪)"]])

# --- תקציר מספרי ---
st.subheader("📊 סיכום מספרי")

final_balance = balances[-1]
final_deposits = deposits_total[-1]
profit = final_balance - final_deposits

col3, col4, col5 = st.columns(3)

with col3:
    st.metric("שווי סופי של התיק", f"{final_balance:,.0f} ₪")

with col4:
    st.metric("סך כל ההפקדות", f"{final_deposits:,.0f} ₪")

with col5:
    st.metric("רווח/הפסד", f"{profit:,.0f} ₪")

st.caption("החישוב מניח תשואה חודשית קבועה (ריבית דריבית) והפקדה בסוף כל חודש.")
