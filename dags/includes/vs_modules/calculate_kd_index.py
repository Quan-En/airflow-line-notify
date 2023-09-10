import pandas as pd

def calculateKDIndex(df: pd.DataFrame) -> pd.DataFrame:
    df["rsv"] = df['close']-df['close'].rolling(window=9).min()
    df["rsv"] = df["rsv"] / (df['close'].rolling(window=9).max() - df['close'].rolling(window=9).min()) * 100
    
    # df["rsv"] = df['Close']-df['Close'].rolling(window=9).min()
    # df["rsv"] = df["rsv"] / (df['Close'].rolling(window=9).max() - df['Close'].rolling(window=9).min()) * 100
    df = df.dropna()

    K = 50 # init
    D = 50 # init
    k_list = []
    for v in df["rsv"]:
        new_k = K * (2 / 3) + v * (1 / 3)
        k_list.append(new_k)
        K = new_k
    D_list = []
    for v in k_list:
        new_d = D* (2 / 3) + v * (1 / 3)
        D_list.append(new_d)
        D = new_d

    return pd.concat([
        df, 
        pd.DataFrame({"K":k_list}, index=df.index), 
        pd.DataFrame({"D":D_list}, index=df.index)
    ], axis=1)