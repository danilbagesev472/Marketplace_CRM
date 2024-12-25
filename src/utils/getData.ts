import axios from 'axios'

export function getData() {
	const data = fetch('https://api.example.com/data').then(response =>
		response.json()
	)
	return data
}

export function getData2() {
	const data = axios.get('https://api.example.com/data')
	return data
}

export function getData3(id: string) {
	const data = axios.get(`https://api.example.com/data/${id}`)
	return data
}
