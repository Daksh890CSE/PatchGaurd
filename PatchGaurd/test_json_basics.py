import json

def test_dictionary_to_json():
    finding ={
        "function":"withdraw",
        "severity":"medium"
    }

    result=json.dumps(finding)

    assert isinstance(result,str)
    assert '"function": "withdraw"' in result

def test_json_to_dictionary():
    json_string='{"function":"withdraw","severity":"medium"}'
    result=json.loads(json_string)

    assert isinstance(result,dict)
    assert result["function"]=="withdraw"
    assert result["severity"]=="medium"