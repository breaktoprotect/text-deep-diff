sentences_to_compare_dataset = [
    {
        "description": "Similar English text True",
        "first_sentence": "Regular exercise strengthens the heart and improves overall health.",
        "second_sentence": "Engaging in physical activities like jogging or swimming helps maintain cardiovascular fitness.",
    },
    {
        "description": "Similar English text False",
        "first_sentence": "Regular exercise strengthens the heart and improves overall health.",
        "second_sentence": "Watching movies is a great way to relax and unwind.",
    },
    {
        "description": "Matching configuration setting to MITRE ATT&CK technique True",
        "first_sentence": "T1557.001 - LLMNR/NBT-NS Poisoning and SMB Relay",
        "second_sentence": "Ensure 'Turn off multicast name resolution' is set to 'Enabled' to mitigate LLMNR and NetBIOS Name Service spoofing attacks.",
    },
    {
        "description": "Matching configuration setting to MITRE ATT&CK technique False",
        "first_sentence": "T1557.001 - LLMNR/NBT-NS Poisoning and SMB Relay",
        "second_sentence": "Ensure 'Guest account status' is set to 'Enabled' to facilitate easier access for shared resources.",
    },
    {
        "description": "Cyber Security GRC Categorization True",
        "first_sentence": "Endpoint Protection and Threat Management",
        "second_sentence": "All endpoint devices and servers must be protected by enterprise-grade EDR and antivirus solutions, ensuring continuous threat monitoring, detection, and response in compliance with regulatory and internal security requirements.",
    },
    {
        "description": "Cyber Security GRC Categorization False",
        "first_sentence": "Endpoint Protection and Threat Management",
        "second_sentence": "All privileged accounts must use multi-factor authentication (MFA) to prevent unauthorized access.",
    },
    {
        "description": "Subset test True",
        "first_sentence": "The list of acceptable cipher suites: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_AES_128_GCM_SHA256",
        "second_sentence": "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
    },
    {
        "description": "Subset test False",
        "first_sentence": "The list of acceptable cipher suites: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_AES_128_GCM_SHA256",
        "second_sentence": "TLS_RSA_WITH_3DES_EDE_CBC_SHA",
    },
]
