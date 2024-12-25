<script setup lang="js">
import axios from 'axios'

defineProps({
      name: string,
      id: number,
      img: string,
      brand: string,
      price: number,
})

const data = axios.get('https://fakestoreapi.com/products')
</script>

<template>
	<div class="product">
		<img :src="data.img" alt="Product Image" />
		<h2>{{ name }}</h2>
		<p>{{ brand }}</p>
		<p>${{ price }}</p>
		<button @click="addToCart">Add to Cart</button>
	</div>
</template>

<style scoped></style>
