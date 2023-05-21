import { Image } from "../models/responses";

const IP = "http://127.0.0.1:5002/"
const CAR_RESULT_INFO = IP + "car-dataset-info"
const TEST_MODEL = IP + "test-car-model"

const requestFileOptions = (file: any) => ({
    method: 'POST',
    body: file
});

export const fetchCarDatasetInfo = () => {
  return fetch(CAR_RESULT_INFO)
    .then(response => response.json())
}

export const fetchCarModelTesting = (image : Image) => {
  const body = new FormData();
  body.append("file", image.value);
  return fetch(TEST_MODEL, requestFileOptions(body))
    .then(response => response.json())
}