import pytest
<<<<<<< HEAD
from unittest.mock import MagicMock, patch
from Analysis import Analysis

@pytest.fixture
def analysis_obj():
    return Analysis('configs/job_file.yml')

def test_load_config(analysis_obj):
    # Mock the return value of yaml.safe_load
    with patch('analysis.yaml.safe_load') as mock_safe_load:
        mock_safe_load.return_value = {'project': 'nightlock'}

        # Call the load_config method
        config = analysis_obj.load_config(['configs/system_config.yml', 'configs/user_config.yml'])

        # Check if yaml.safe_load is called with the correct arguments
        mock_safe_load.assert_called_once_with(MagicMock.ANY)

        # Check if the config is loaded correctly
        assert config == {'project': 'nightlock'}

def test_load_data_with_valid_url(analysis_obj):
    # Mocking requests.get to return a MagicMock object
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {'data': 'mocked_data'}

    # Mocking the requests.get function
    with patch('analysis.requests.get') as mock_get:
        mock_get.return_value = mock_response

        # Call the load_data method
        analysis_obj.load_data()

        # Check if requests.get is called with the correct URL
        mock_get.assert_called_once_with(analysis_obj.config['kaggle_dataset_url'])

        # Check if the dataset is loaded correctly
        assert analysis_obj.dataset == {'data': 'mocked_data'}

def test_load_data_with_invalid_url(analysis_obj):
    # Modify the configuration to have an invalid URL
    analysis_obj.config['kaggle_dataset_url'] = ''

    # Call the load_data method and expect a ValueError
    with pytest.raises(ValueError):
        analysis_obj.load_data()

def test_compute_analysis_with_no_data(analysis_obj):
    # Modify the dataset attribute to be None
    analysis_obj.dataset = None

    # Call the compute_analysis method and expect a ValueError
    with pytest.raises(ValueError):
        analysis_obj.compute_analysis()

def test_compute_analysis_with_valid_data(analysis_obj):
    # Mock the dataset attribute
    analysis_obj.dataset = MagicMock()
    analysis_obj.dataset.groupby.return_value.sum.return_value.reset_index.return_value = {'data': 'mocked_output'}

    # Call the compute_analysis method
    result = analysis_obj.compute_analysis()

    # Check if the method returns the correct result
    assert result == {'data': 'mocked_output'}

def test_notify_done(analysis_obj):
    # Mock the requests.post function
    with patch('analysis.requests.post') as mock_post:
        mock_post.return_value.raise_for_status.return_value = None

        # Call the notify_done method
        analysis_obj.notify_done("Mocked message")

        # Check if requests.post is called with the correct arguments
        mock_post.assert_called_once_with(
            f"https://ntfy.sh/{analysis_obj.config['ntfy_topic']}",
            data="Mocked message".encode(encoding='utf-8')
        )

def test_plot_data_with_no_dataset(analysis_obj):
    # Modify the dataset attribute to be None
    analysis_obj.dataset = None

    # Call the plot_data method and expect a ValueError
    with pytest.raises(ValueError):
        analysis_obj.plot_data()

# Add more test cases as needed
=======
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
>>>>>>> a633c95 (Updated commit)
