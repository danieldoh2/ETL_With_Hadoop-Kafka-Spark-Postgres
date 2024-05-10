import pytest
from unittest.mock import patch, MagicMock, ANY
import json
from adapted_kafka import process_message, connect_db, create_table

# Now we mock the environment variables


@patch.dict('os.environ', {
    'POSTGRES_HOST': 'localhost',
    'POSTGRES_USER': 'user',
    'POSTGRES_PASSWORD': 'password',
    'POSTGRES_DB': 'mydb'
})
@patch('adapted_kafka.psycopg2.connect')
def test_connect_db(mock_connect):
    mock_connect.return_value = MagicMock()
    connection = connect_db()
    assert mock_connect.called
    assert connection is not None

# Test the message processing function


@patch('adapted_kafka.psycopg2.connect')
def test_process_message(mock_connect):
    # Setup the mock
    conn = mock_connect.return_value.__enter__.return_value
    cursor = conn.cursor.return_value

    # Example message data
    msg_data = {
        'Details': 'Example event',
        'Location': 'Location1',
        'Severity': 'High',
        'EventType': 'Type1',
        'Timestamp': '2023-01-01 12:00:00'
    }

    # Convert to Kafka message format
    msg = MagicMock()
    msg.value.return_value.decode.return_value = json.dumps(msg_data)
    msg.error.return_value = None

    # Call the function that processes the message
    process_message(msg, cursor)

    # Check that the cursor executed with the right SQL
    cursor.execute.assert_called_with(ANY, (ANY, ANY, ANY, ANY, ANY, ANY, ANY))

# Test to ensure that table creation runs without errors


@patch('adapted_kafka.psycopg2.connect')
def test_create_table(mock_connect):
    conn = mock_connect.return_value.__enter__.return_value
    cursor = conn.cursor.return_value

    create_table(cursor)
    cursor.execute.assert_called_once()
