import streamlit as st
from PIL import Image
import easyocr
import numpy as np

# Title aur description
st.set_page_config(page_title="Mom's Hindi Question Paper Maker", page_icon="📝")
st.title("📚 Mom's Hindi OCR Tool")
st.markdown("**Book ki photo upload karo → Hindi text turant type ho jayega!**")

# Reader ko cache kar diya (fast rahega)
@st.cache_resource
def get_reader():
    return easyocr.Reader(['hi', 'en'], gpu=False)  # gpu=True agar NVIDIA card hai to

reader = get_reader()

# Upload section
uploaded_file = st.file_uploader("Book ka page ki photo upload karo (JPG/PNG)", 
                               type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Image show karo
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Photo", use_column_width=True)
    
    # Button
    if st.button("🔥 Extract Hindi Text", type="primary"):
        with st.spinner("Text nikal raha hai... thoda wait karo (pehle baar 10-15 sec lagega)"):
            # PIL se numpy array banao
            img_array = np.array(image)
            
            # OCR chalao
            results = reader.readtext(img_array, detail=0, paragraph=True)
            
            # Saare paragraphs ko join kar do
            extracted_text = "\n\n".join(results)
            
            # Result dikhayo
            st.success("✅ Text nikal gaya!")
            st.subheader("📝 Extracted Text (edit kar sakte ho)")
            
            text_area = st.text_area("Yahan se copy-paste kar lo", 
                                   value=extracted_text, 
                                   height=400)
            
            # Download button
            st.download_button(
                label="📥 Download as .txt file",
                data=text_area.encode("utf-8"),
                file_name="question_paper_hindi.txt",
                mime="text/plain"
            )
            
            st.info("Tip: Agar koi galti ho to text area mein khud theek kar lo.")

# Footer
st.caption("Made with ❤️ for your mom | Ash ka beta banaya 😎")