import data

def test_merged_df():
    d = data.Data()
    df = d.merged_df
    assert not df.empty, "There is no data."