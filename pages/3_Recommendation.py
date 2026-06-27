
import streamlit as st
import pickle

st.set_page_config(page_title="Property Recommendation", page_icon="🏠", layout="wide")
st.title("🏠 Gurgaon Property Recommendation")

with open("datasets/df_recom.pkl","rb") as f: df_recom=pickle.load(f)
with open("datasets/location_distance.pkl","rb") as f: location_df=pickle.load(f)
with open("datasets/price_bhk_df.pkl","rb") as f: price_bhk_df=pickle.load(f)
with open("datasets/cosine_sim1.pkl","rb") as f: cosine_sim1=pickle.load(f)
with open("datasets/cosine_sim2.pkl","rb") as f: cosine_sim2=pickle.load(f)
with open("datasets/cosine_sim3.pkl","rb") as f: cosine_sim3=pickle.load(f)

property_to_index=dict(zip(df_recom["PropertyName"],df_recom.index))
if "candidate_societies" not in st.session_state:
    st.session_state.candidate_societies=[]

c1,c2=st.columns(2)
with c1:
    loc=st.selectbox("Location",sorted(location_df.columns))
    bhk=st.selectbox("BHK",sorted(price_bhk_df["bhk"].unique()))
with c2:
    radius=st.slider("Radius (m)",500,60000,15000,500)
    mn,mx=st.slider("Budget (Cr)",0.5,50.0,(2.0,4.0),0.25)

if st.button("Recommend Properties"):
    nearby=location_df.index[location_df[loc]<=radius].tolist()
    budget=price_bhk_df[(price_bhk_df.bhk==bhk)&(price_bhk_df.price_min<=mx)&(price_bhk_df.price_max>=mn)]["society"].unique().tolist()
    st.session_state.candidate_societies=sorted(list(set(nearby)&set(budget)))

if st.session_state.candidate_societies:
    selected=st.selectbox("Select Property",st.session_state.candidate_societies)
    if st.button("Show Similar Properties"):
        idx=property_to_index[selected]
        final=0.45*cosine_sim1[idx]+0.35*cosine_sim2[idx]+0.20*cosine_sim3[idx]
        scores=sorted(list(enumerate(final)),key=lambda x:x[1],reverse=True)
        st.subheader("Top 5 Similar Properties")
        shown=0
        for ridx,score in scores:
            if ridx==idx:
                continue
            row=df_recom.iloc[ridx]
            bhk_df=price_bhk_df[(price_bhk_df.society==row["PropertyName"])&(price_bhk_df.bhk==bhk)]
            if bhk_df.empty:
                continue
            p=bhk_df.iloc[0]
            st.markdown(f"### {shown+1}. {row['PropertyName']}")
            # st.write(f"Similarity: {score:.3f}")
            st.write(row["PropertySubName"])
            st.write(f"Price: ₹{p['price_min']} - ₹{p['price_max']} Cr")
            # st.write(row["TopFacilities"])
            st.write(row["Link"])
            st.divider()
            shown+=1
            if shown==5:
                break
