---

excalidraw-plugin: parsed
tags: [excalidraw]

---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'


# Excalidraw Data

## Text Elements
Transaction

- id (primary, text)
- type (text)
- category_id (foreign -> category)
- amount (real)
- time (real)
- notes (text) ^iiPcwfQQ

Budget

- id (primary, text)
- name (primary, text)
- category_id (foreign -> category)
- start (real)
- end (real)
- amount (real) ^W4Cshc2U

Collection

- id (primary, text)
- name (text)
- time (real)
- notes (text) ^ZD3R6DXb

Category

- id (primary, text)
- name (text) ^eEln9tAL

Collection-Transaction MTM

- id (primary, text)
- collection_id (foreign -> collection)
- transaction_id (foreign -> transaction) ^2jLvGapb

%%
## Drawing
```compressed-json
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=
```
%%