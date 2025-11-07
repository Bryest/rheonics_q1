# app/data/mock.py
def sensor_kpis():
    return {
        "data": 7265,
        "connected": 3,
        "events": 156,

        # Real Data
        "trend_data_this_year": [
            8000, 12000, 9000, 14000, 18000, 11000,
            19000, 15000, 21000, 17000, 22000, 24000
        ],
        "trend_data_last_year": [
            10000, 7000, 11000, 9000, 12000, 10000,
            14000, 13000, 15000, 16000, 18000, 20000
        ],
    }
