import { Image } from "../types/responses";

const IP = "http://127.0.0.1:5000/"
const GET_RESULT = IP + "result"
const UPLOAD_IMAGE = IP + "upload-image"

const requestFileOptions = (file: any) => ({
    method: 'POST',
    body: file
});

export const fetchResult = () => {
  return fetch(GET_RESULT)
    .then(response => response.json())
}

export const fetchUploadImage = (image : Image) => {
  const body = new FormData();
  body.append("file", image.value);
  return fetch(UPLOAD_IMAGE, requestFileOptions(body))
    .then(response => response.json())
}