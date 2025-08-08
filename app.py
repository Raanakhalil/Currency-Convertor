import streamlit as st
import requests


st.set_page_config(page_title="Enhanced Currency Converter", layout="centered")
st.title("💱 Currency Converter with Insights")
st.markdown("Convert currencies with real‐time rates, flags, history, and country insights.")

API_KEY = "f8ba560796180f23ddf7e906"  # ← Replace with your exchangerate-api.com key

# Full metadata for each currency
currency_data = {
    "USD": {"flag": "🇺🇸", "name": "United States Dollar", "country": "United States",
            "proposed_by": "Alexander Hamilton (1792)", "leader": "Joe Biden"},
    "EUR": {"flag": "🇪🇺", "name": "Euro", "country": "European Union",
            "proposed_by": "European Commission (1999)", "leader": "Ursula von der Leyen"},
    "GBP": {"flag": "🇬🇧", "name": "British Pound", "country": "United Kingdom",
            "proposed_by": "King Henry II (12th century)", "leader": "Rishi Sunak"},
    "INR": {"flag": "🇮🇳", "name": "Indian Rupee", "country": "India",
            "proposed_by": "Sher Shah Suri (16th century)", "leader": "Narendra Modi"},
    "PKR": {"flag": "🇵🇰", "name": "Pakistani Rupee", "country": "Pakistan",
            "proposed_by": "State Bank of Pakistan (1948)", "leader": "Shehbaz Sharif"},
    "AUD": {"flag": "🇦🇺", "name": "Australian Dollar", "country": "Australia",
            "proposed_by": "Reserve Bank of Australia (1966)", "leader": "Anthony Albanese"},
    "CAD": {"flag": "🇨🇦", "name": "Canadian Dollar", "country": "Canada",
            "proposed_by": "Bank of Canada (1935)", "leader": "Justin Trudeau"},
    "SGD": {"flag": "🇸🇬", "name": "Singapore Dollar", "country": "Singapore",
            "proposed_by": "Monetary Authority of Singapore", "leader": "Tharman Shanmugaratnam"},
    "JPY": {"flag": "🇯🇵", "name": "Japanese Yen", "country": "Japan",
            "proposed_by": "Meiji Government (1871)", "leader": "Fumio Kishida"},
    "CNY": {"flag": "🇨🇳", "name": "Chinese Yuan", "country": "China",
            "proposed_by": "People's Bank of China (1948)", "leader": "Xi Jinping"},
    "CHF": {"flag": "🇨🇭", "name": "Swiss Franc", "country": "Switzerland",
            "proposed_by": "Swiss National Bank (1907)", "leader": "Alain Berset"},
    "NZD": {"flag": "🇳🇿", "name": "New Zealand Dollar", "country": "New Zealand",
            "proposed_by": "Reserve Bank of New Zealand (1934)", "leader": "Chris Hipkins"},
    "SEK": {"flag": "🇸🇪", "name": "Swedish Krona", "country": "Sweden",
            "proposed_by": "Riksbank (1873)", "leader": "Ulf Kristersson"},
    "NOK": {"flag": "🇳🇴", "name": "Norwegian Krone", "country": "Norway",
            "proposed_by": "Norwegian Central Bank (1875)", "leader": "Jonas Gahr Støre"},
    "DKK": {"flag": "🇩🇰", "name": "Danish Krone", "country": "Denmark",
            "proposed_by": "Nationalbanken (1875)", "leader": "Mette Frederiksen"},
    "ZAR": {"flag": "🇿🇦", "name": "South African Rand", "country": "South Africa",
            "proposed_by": "South African Reserve Bank (1961)", "leader": "Cyril Ramaphosa"},
    "AED": {"flag": "🇦🇪", "name": "UAE Dirham", "country": "United Arab Emirates",
            "proposed_by": "Central Bank of UAE (1973)", "leader": "Mohammed bin Zayed"},
    "SAR": {"flag": "🇸🇦", "name": "Saudi Riyal", "country": "Saudi Arabia",
            "proposed_by": "Saudi Arabian Monetary Authority", "leader": "Mohammed bin Salman"},
    "HKD": {"flag": "🇭🇰", "name": "Hong Kong Dollar", "country": "Hong Kong",
            "proposed_by": "Hong Kong Monetary Authority", "leader": "John Lee"},
    "THB": {"flag": "🇹🇭", "name": "Thai Baht", "country": "Thailand",
            "proposed_by": "Bank of Thailand (1942)", "leader": "Srettha Thavisin"},
    "KRW": {"flag": "🇰🇷", "name": "South Korean Won", "country": "South Korea",
            "proposed_by": "Bank of Joseon (1902)", "leader": "Han Duck-soo"},
    "RUB": {"flag": "🇷🇺", "name": "Russian Ruble", "country": "Russia",
            "proposed_by": "Peter the Great (1704)", "leader": "Vladimir Putin"},
    "BRL": {"flag": "🇧🇷", "name": "Brazilian Real", "country": "Brazil",
            "proposed_by": "Central Bank of Brazil (1994)", "leader": "Luiz Inácio Lula da Silva"},
    "MXN": {"flag": "🇲🇽", "name": "Mexican Peso", "country": "Mexico",
            "proposed_by": "Banco de México (1925)", "leader": "Andrés Manuel López Obrador"},
    "IDR": {"flag": "🇮🇩", "name": "Indonesian Rupiah", "country": "Indonesia",
            "proposed_by": "Bank Indonesia (1946)", "leader": "Joko Widodo"},
    "TRY": {"flag": "🇹🇷", "name": "Turkish Lira", "country": "Turkey",
            "proposed_by": "Ottoman Empire (1844)", "leader": "Recep Tayyip Erdoğan"},
    "PLN": {"flag": "🇵🇱", "name": "Polish Zloty", "country": "Poland",
            "proposed_by": "National Bank of Poland (1924)", "leader": "Donald Tusk"},
    "CZK": {"flag": "🇨🇿", "name": "Czech Koruna", "country": "Czech Republic",
            "proposed_by": "Czech National Bank (1993)", "leader": "Petr Fiala"},
    "HUF": {"flag": "🇭🇺", "name": "Hungarian Forint", "country": "Hungary",
            "proposed_by": "Hungarian National Bank (1946)", "leader": "Viktor Orbán"},
    "MYR": {"flag": "🇲🇾", "name": "Malaysian Ringgit", "country": "Malaysia",
            "proposed_by": "Bank Negara Malaysia (1975)", "leader": "Anwar Ibrahim"},
    "PHP": {"flag": "🇵🇭", "name": "Philippine Peso", "country": "Philippines",
            "proposed_by": "Central Bank of the Philippines (1949)", "leader": "Ferdinand Marcos Jr."},
    "EGP": {"flag": "🇪🇬", "name": "Egyptian Pound", "country": "Egypt",
            "proposed_by": "National Bank of Egypt (1834)", "leader": "Abdel Fattah el-Sisi"},
    "BDT": {"flag": "🇧🇩", "name": "Bangladeshi Taka", "country": "Bangladesh",
            "proposed_by": "Bangladesh Bank (1972)", "leader": "Sheikh Hasina"},
    "VND": {"flag": "🇻🇳", "name": "Vietnamese Dong", "country": "Vietnam",
            "proposed_by": "State Bank of Vietnam (1978)", "leader": "Phạm Minh Chính"},
    "NGN": {"flag": "🇳🇬", "name": "Nigerian Naira", "country": "Nigeria",
            "proposed_by": "Central Bank of Nigeria (1973)", "leader": "Bola Tinubu"},
    "ARS": {"flag": "🇦🇷", "name": "Argentine Peso", "country": "Argentina",
            "proposed_by": "Banco Central de la República Argentina (1992)", "leader": "Sergio Massa"},
    "ILS": {"flag": "🇮🇱", "name": "Israeli Shekel", "country": "Israel",
            "proposed_by": "Bank of Israel (1985)", "leader": "Benjamin Netanyahu"},
    "KWD": {"flag": "🇰🇼", "name": "Kuwaiti Dinar", "country": "Kuwait",
            "proposed_by": "Central Bank of Kuwait (1961)", "leader": "Ahmad Nawaf Al-Ahmad Al-Sabah"},
    "QAR": {"flag": "🇶🇦", "name": "Qatari Riyal", "country": "Qatar",
            "proposed_by": "Qatar Central Bank (1973)", "leader": "Mohammed bin Abdulrahman Al Thani"},
    "BHD": {"flag": "🇧🇭", "name": "Bahraini Dinar", "country": "Bahrain",
            "proposed_by": "Central Bank of Bahrain (2006)", "leader": "Khalifa bin Salman"},
    "OMR": {"flag": "🇴🇲", "name": "Omani Rial", "country": "Oman",
            "proposed_by": "Central Bank of Oman (1970)", "leader": "Haitham bin Tariq"},
    "CLP": {"flag": "🇨🇱", "name": "Chilean Peso", "country": "Chile",
            "proposed_by": "Banco Central de Chile (1960)", "leader": "Gabriel Boric"},
    "COP": {"flag": "🇨🇴", "name": "Colombian Peso", "country": "Colombia",
            "proposed_by": "Banco de la República (1871)", "leader": "Gustavo Petro"},
    "TWD": {"flag": "🇹🇼", "name": "New Taiwan Dollar", "country": "Taiwan",
            "proposed_by": "Central Bank of the Republic of China (1949)", "leader": "William Lai"},
    "RON": {"flag": "🇷🇴", "name": "Romanian Leu", "country": "Romania",
            "proposed_by": "National Bank of Romania (1867)", "leader": "Nicolae Ciucă"},
    "LKR": {"flag": "🇱🇰", "name": "Sri Lankan Rupee", "country": "Sri Lanka",
            "proposed_by": "Ceylon Government (1872)", "leader": "Ranil Wickremesinghe"},
    "MAD": {"flag": "🇲🇦", "name": "Moroccan Dirham", "country": "Morocco",
            "proposed_by": "Bank Al-Maghrib (1959)", "leader": "Aziz Akhannouch"},
    "UAH": {"flag": "🇺🇦", "name": "Ukrainian Hryvnia", "country": "Ukraine",
            "proposed_by": "National Bank of Ukraine (1996)", "leader": "Denys Shmyhal"},
    "KES": {"flag": "🇰🇪", "name": "Kenyan Shilling", "country": "Kenya",
            "proposed_by": "Central Bank of Kenya (1966)", "leader": "William Ruto"}
}

currency_list = list(currency_data.keys())

# Conversion logic
def convert_currency(amount, from_cur, to_cur):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_cur}/{to_cur}/{amount}"
    try:
        r = requests.get(url, timeout=10)
        d = r.json()
        if d.get("result") == "success":
            return round(d["conversion_result"], 2)
        else:
            return f"API Error: {d.get('error-type', 'Unknown error')}"
    except Exception as e:
        return f"Request failed: {e}"

# Session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# UI: selectors
col1, col2 = st.columns(2)
with col1:
    from_cur = st.selectbox(
        "From", currency_list,
        format_func=lambda c: f"{currency_data[c]['flag']} {c} — {currency_data[c]['name']}"
    )
with col2:
    to_cur = st.selectbox(
        "To", currency_list,
        format_func=lambda c: f"{currency_data[c]['flag']} {c} — {currency_data[c]['name']}"
    )

amount = st.number_input("Amount", min_value=0.0, value=1.0, step=0.1)

if st.button("Convert"):
    res = convert_currency(amount, from_cur, to_cur)
    if isinstance(res, (int, float)):
        st.success(f"{amount} {from_cur} = {res} {to_cur}")
        st.session_state.history.insert(0, f"{amount} {from_cur} → {res} {to_cur}")
        st.session_state.history = st.session_state.history[:5]
    else:
        st.error(res)

# Show history
if st.session_state.history:
    st.divider()
    st.markdown("### 📜 Recent Conversions")
    for h in st.session_state.history:
        st.write(h)

# Show details
st.divider()
st.markdown("### 🌍 Currency Details")
c1, c2 = st.columns(2)
with c1:
    d = currency_data[from_cur]
    st.subheader(f"{d['flag']} {from_cur} — {d['name']}")
    st.write(f"**Country:** {d['country']}")
    st.write(f"**Leader:** {d['leader']}")
    st.write(f"**Proposed By:** {d['proposed_by']}")
with c2:
    d = currency_data[to_cur]
    st.subheader(f"{d['flag']} {to_cur} — {d['name']}")
    st.write(f"**Country:** {d['country']}")
    st.write(f"**Leader:** {d['leader']}")
    st.write(f"**Proposed By:** {d['proposed_by']}")
