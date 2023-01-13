<script>
	import { onMount } from 'svelte';
	import { Card, Input, Button, ButtonGroup, InputGroup, Spinner, Popover, Icon } from 'sveltestrap/src'

	const endpoint = 'https://api.koczulap.pl'
	let prompt = ''
	let convId = ''
	let messages = []
	let button_enabled = false
	let dream_enabled = false

	onMount(async function() {
		let response = await fetch(endpoint + '/init')
		let data = await response.json()
		convId = data['conv_id']
		button_enabled = true
		response = await fetch(endpoint + '/functionality')
		data = await response.json()
		if (data['txt2img']) {
			dream_enabled = true
		}
	})

	async function doPost () {
		button_enabled = false
		messages.push({
			"type": "text",
			"data": prompt
		})
		let msg = prompt
		prompt = ''
		messages = messages
		console.log(msg)
		const res = await fetch(endpoint + '/generate' + '?conv_id=' + convId +'&prompt=' + msg, {
			method: 'GET',
		})
		
		const json = await res.json()
		console.log(json)
		messages.push({
			"type": "text",
			"data": json['response']
		})
		messages = messages
		button_enabled = true
	}
	async function genImage () {
		button_enabled = false
		messages.push({
			"type": "text",
			"data": 'Dream about your last message'
		})
		messages = messages
		const res = await fetch(endpoint + '/txt2img' + '?conv_id=' + convId +'&prompt=' + messages[messages.length - 2]['data'], {
			method: 'GET',
		})
		const img = await res.blob()
		messages.push({
			"type": "img",
			"data": URL.createObjectURL(img)
		})
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
		<div>
			{#each messages as message, i}
				{#if i % 2 == 0}
					<div class='user_msg'>
						<Card body color='light'>{message['data']}</Card>
					</div>
				{:else}
					<div class='bot_msg'>
						{#if message['type'] == "text"}
							<Card body color='info'>{message['data']}</Card>
						{:else}
							<Card body color='info'><img src="{message['data']}" width="256px" alt="Generated image"></Card>
						{/if}
					</div>
				{/if}
			{/each}
			<div class='bot_msg'>
				{#if button_enabled == false}
					<Card body color='info'><Spinner size='sm'/></Card>
				{/if}
			</div>
		</div>
	</div>
	<div id='send_msg'>
		<InputGroup>

			<Input type="text" name="text" placeholder='Say hello!' bind:value={prompt}/>
			<ButtonGroup>
				{#if button_enabled == true}
					<Button id='eyo' on:click={doPost}><Icon name="send-fill"/></Button>
					{#if dream_enabled == true}
						<Button on:click={genImage}><Icon name="image-fill"/></Button>
					{:else}
						<span id='dream-btn'><Button disabled id='dream-btn' on:click={genImage}>Dream</Button></span>
						<Popover
							trigger="hover"
							placement="top"
							target="dream-btn"
							>
							No GPU backend detected
						</Popover>
					{/if}
				{:else}
					<Button disabled on:click={doPost}><Icon name="send-fill"/></Button>
					<Button disabled on:click={genImage}><Icon name="image-fill"/></Button>
				{/if}
			</ButtonGroup>
		</InputGroup>
</div>
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
		padding-bottom: 10px;
		padding-top: 10px;
	}
	#chat {
		width: 80%;
		max-width: 80%;
		height: 10px;
		flex-grow: 1;
		overflow-y: scroll;
		scroll-snap-type: y proximity;
		display: flex;
		flex-direction: column-reverse;
	}

</style>
