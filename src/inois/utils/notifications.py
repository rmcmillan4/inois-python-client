class Notifications:
    FILE_NOT_FOUND_ERROR = "File '{0}' was not found"
    INVALID_INPUT_FILE_FORMAT_ERROR = "Input file format is invalid for file: {0}. Can't convert input to type 'dictionary'"
    INVALID_KEY_ERROR = "Key type '{0}' is not supported"
    INVALID_CONFIG_VALUE_TYPE_ERROR = "Value for config key '{0}' must be a '{1}', but '{2}' is a {3}"
    INVALID_LIST_ITEM_TYPE_ERROR = "List items for '{0}' must be {1}, but '{2}' is a {3}"
    DIRECTORY_NOT_FOUND_ERROR = "Directory '{0}' was not found."
    ACTIVE_WORKING_DIRECTORY = "Working directory: {0}"
    FILE_FOUND = "Located file: {0}"
    NO_CSV_FILES_FOUND_IN_FOLDER_ERROR = "No csv files were found in folder {0}"
    NON_CSV_FILE_EXTENSION_ERROR = "Invalid file extension detected for file {0}, only '.csv' files are supported"
    EMPTY_CSV_FILE_ERROR = "Failed to find data to parse from csv file {0}"
    INVALID_CSV_FILE_FORMAT_ERROR = "Failed to parse file {0} as a csv file. Ensure '{0}' is in csv format and/or that the csv delimeter character '{1}' is valid"
    COLUMN_TO_HASH_NOT_FOUND_ERROR = "Failed to locate column '{0}' in csv file '{1}'. Ensure column '{0}' exists and/or that the csv delimeter character '{2}' is valid"
    CURRENT_FILE = "Current file: '{0}'"
    HASHING_FILES = "Hashing csv files..."
    HASHING_SUCCESSFUL = "hashing successful, file '{0}' created"
    AUTHENTICATION_SUCCESSFUL = "Authentication successful"
    PREVIOUS_SESSION_IN_CACHE = "Previous application session detected, attempting authentication via refresh token"
    AUTHENTICATION_REQUIRED = "No previous application sessions found, authentication is required"
    ENCRYPTING_FILES = "Encrypting hashed csv files..."
    ENCRYPTION_SUCCESSFUL = "encryption successful, file '{0}' created"
    REQUIRED_CONFIG_KEY_NOT_FOUND_ERROR = "Failed to locate required config key '{0}' in the application config file"
    FETCHING_API_KEYS = "Fetching salt and encryption keys from the inois api..."
    API_KEY_FETCH_ERROR = "An error occured while fetching the salt and encryption keys from the api.  The server returned a response of '{0}'"
    API_KEY_FETCH_RESPONSE_FORMAT_ERROR = "The response from the api key fetch did not include required key '{0}'"
    EMPTY_SALT_KEY_ERROR = "The list of salt keys returned by the api is empty"
    API_KEY_FETCH_SUCCESSFUL = "successfully fetched salt and encryption keys"
    UPLOADING_FILES = "Uploading encrypted files to the inois api.."
    FILE_SUCCESSFULLY_UPLOADED = "{0} successfully uploaded with batch id '{1}'"
    FILE_UPLOAD_FAILED = "Failed to upload file {0}, the server returned a response of '{1}'"
    INVALID_DATE_FORMAT_ERROR = "Invalid date format '{0}' detected for key {1}.  A value with format 'MM-DD-YYYY' (e.g., '09-09-2019') is required"
    HASHING_SEARCH_ENTRIES = "Hashing search data..."
    HASHING_SEARCH_ENTRIES_SUCCESSFUL = "successfully hashed search entries to query for file '{0}'"
    EXECUTING_SEARCH = "Executing search queries using hashed data..."
    CURRENT_DATUM_QUERY = "Current datum query: {0}"
    DATUM_QUERY_FAILED = "Failed to query datum {0}, the server returned a response of '{1}'"
    DATUM_QUERY_SUCCESSFUL = "Successfully queried datum. {0} record(s) located:"
    CHUNKING_FILES = "Chunking csv files..."
    CHUNKING_SUCCESSFUL = "chunking successful, file '{0}' will be processed as {1} chunk(s)"
    APPLICATION_STARTED = "INOIS application Started in '{0}' mode at {1}"
    APPLICATION_TERMINATED = "INOIS application terminated successfully at {0}"
