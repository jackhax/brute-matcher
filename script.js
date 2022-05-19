console.log('logging');

let details = document.getElementById("div");
console.log(details)
async function getData(url,element){
  data = await fetch(url,{
    method: "GET",
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
      "Content-Type": "application/json",
      'accept': 'application/json'
    }}).then(async (res) => res.json()).then(data =>element.innerHTML = data);
    return data
}

getData(`https://y7kapglool.execute-api.ap-south-1.amazonaws.com/brute-matcher?action=listall&id=dee412`,details)

async function match(){
  let mem_id = document.getElementById('mem_id')
  mem_id = mem_id.value;
  console.log(mem_id)
  await getData(`https://y7kapglool.execute-api.ap-south-1.amazonaws.com/brute-matcher?action=match&id=${mem_id}`,document.getElementById('res'))
  getData(`https://y7kapglool.execute-api.ap-south-1.amazonaws.com/brute-matcher?action=listall&id=dee412`,details)

}
