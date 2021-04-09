# MccM_Utilities

Scripts to prepare requests to be injected to McM

- Modify template files to change necessary info such as gridpack paths and fragmanets etc.
- Run "python create_requests.py" to generate csv files which contain all the request info
- When csv files are ready, run "source getCookie.sh" in root directory to get authentication
- Clone a request in the same campaign on McM
- Clone and inject the requests to McM from the csv files by doing (can test w/o submission by the --dry option):
  "python manageRequests.py <path_to_csv> --clone <prep_id_for_the_request_you_cloned_on_McM>"
