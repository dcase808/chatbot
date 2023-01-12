<script>
	import { onMount } from 'svelte';
	import { Card, FormGroup, Input, Button } from 'sveltestrap/src'

	const endpoint = 'http://localhost:9973'

	let prompt = ''

	let convId = ''

	let messages = []

	let button_enabled = true

	onMount(async function() {
		const response = await fetch(endpoint + '/init')
		const data = await response.json()
		convId = data['conv_id']
	})

	async function doPost () {
		button_enabled = false
		messages.push(prompt)
		messages = messages
		const res = await fetch(endpoint + '/generate' + '?conv_id=' + convId +'&prompt=' + prompt, {
			method: 'POST',
		})
		
		const json = await res.json()
		console.log(json)
		messages.push(json['response'])
		messages = messages
		button_enabled = true
	}
	async function genImage () {
		button_enabled = false
		messages.push('Dream about your last message')
		messages = messages
		const res = await fetch(endpoint + '/txt2img' + '?conv_id=' + convId +'&prompt=' + messages[messages.length - 1], {
			method: 'POST',
		})
		const img = await res.blob()
		messages.push(URL.createObjectURL(img))
		const imageObjectURL = URL.createObjectURL(img);
		console.log(imageObjectURL)
		messages = messages
		button_enabled = true
	}


</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	{convId}
	<div id='chat'>
		{#each messages as message, i}
			{#if i % 2 == 0}
				<div class='user_msg'>
					<Card body color='light'>{message}</Card>
				</div>
			{:else}
				<div class='bot_msg'>
					<Card body color='info'>{message}</Card>
				</div>
			{/if}
		{/each}

	</div>
	<div id='send_msg'>
		<FormGroup>
			<Input type="search" name="text" id="exampleText" placeholder='Say hello!' bind:value={prompt} />
		</FormGroup>
	</div>
	{#if button_enabled == true}
		<Button on:click={doPost}>Send</Button>
		<Button on:click={genImage}>Dream</Button>
	{:else}
		<Button disabled on:click={doPost}>Send</Button>
		<Button disabled on:click={genImage}>Dream</Button>
	{/if}
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		align-items: center;
		flex: 1;
		border: 2px solid black;
		border-radius: 5px;
		height: 100%;
		max-height: 100%;
		padding: 10px;
		width: 100%;
	}

	h1 {
		top: auto;
	}
	.user_msg {
		padding-top: 10px;
		margin-left: 100px;
	}
	.bot_msg {
		padding-top: 10px;
		margin-right: 100px;
	}
	#send_msg {
		margin-bottom: auto;
		width: 80%;
		padding-top: 10px;
	}
	#chat {
		width: 80%;
		max-width: 80%;
		height: 100%;
		flex-grow: 1;
		overflow: auto;
	}

</style>
