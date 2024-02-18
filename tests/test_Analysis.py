import pytest
import matplotlib.pyplot as plt
import pandas as pd
import requests
from nightlock.Analysis import Analysis

@pytest.fixture
def analysis_obj():
    # Create an instance of Analysis with a test configuration
    return Analysis('test_config.yml')

def test_load_data(analysis_obj):
    # Test that the data is loaded correctly
    analysis_obj.load_data()
    assert isinstance(analysis_obj.dataset, pd.DataFrame)
    assert len(analysis_obj.dataset) > 0

def test_compute_analysis(analysis_obj):
    # Test that the analysis is computed correctly
    analysis_obj.load_data()
    analysis_output = analysis_obj.compute_analysis()
    assert isinstance(analysis_output, pd.DataFrame)
    assert 'Confirmed' in analysis_output.columns
    assert 'Deaths' in analysis_output.columns

def test_notify_done(analysis_obj, mocker):
    # Mock the requests.post call
    mock_post = mocker.patch('requests.post')
    
    # Configure the mock to return a successful response
    mock_post.return_value.status_code = 200
    
    # Call the method that sends the notification
    ntfy_topic = analysis_obj.config.get('ntfy_topic')
    message = "Testing notification for Analysis"
    response = requests.post(f"https://ntfy.sh/{ntfy_topic}", data=message.encode(encoding='utf-8'))
    
    # Assert that the post request was made with the correct URL
    mock_post.assert_called_once_with(f"https://ntfy.sh/{ntfy_topic}", data=message.encode(encoding='utf-8'))
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, "Notification was not sent successfully"

def test_plot_data(analysis_obj):
    # Test that the plot is created without errors
    analysis_obj.load_data()
    fig = analysis_obj.plot_data()
    assert isinstance(fig, plt.Figure)
