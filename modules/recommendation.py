def recommend_industries(country):

    industry_map = {

        "India":[
            "Renewable Energy",
            "EV Manufacturing",
            "IT Services"
        ],

        "Vietnam":[
            "Electronics Manufacturing",
            "Textile Exports",
            "Semiconductors"
        ],

        "Mexico":[
            "Automobile Manufacturing",
            "Logistics",
            "Electronics"
        ],

        "Brazil":[
            "Agriculture",
            "Mining",
            "Energy"
        ]
    }

    return industry_map.get(
        country,
        ["Technology","Infrastructure","Energy"]
    )
