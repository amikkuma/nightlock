import pytest
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
