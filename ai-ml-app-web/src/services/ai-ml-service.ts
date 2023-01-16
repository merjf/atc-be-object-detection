const IP = "http://127.0.0.1:5000/"
const GET_RESULT = IP + "result"

const requestOptions = (body: any) => ({
    method: 'POST',
    headers: new Headers({
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify(body),
});

export const fetchResult = () => {
  return fetch(GET_RESULT)
    .then(response => response.json())
}

export type Response = {
  value: number[];
  message: string;
};