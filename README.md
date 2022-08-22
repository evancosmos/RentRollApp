# Rent Roll Reader

This is a web app designed to take PDFs or Images of certain Rent Rolls, then parse, calculate, and store them server-side.

## How it works

*TODO: Add diagram*

An image or pdf is uploaded on the front end website. This is passed to either pdfminer.six for pdf reading or pytesseract or image reading. The data is parsed into a json file for calculations and storage on the Firebase Database.