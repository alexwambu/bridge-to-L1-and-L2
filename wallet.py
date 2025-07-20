// wallet_connect.html
<!DOCTYPE html>
<html>
<head>
  <title>Connect Wallet</title>
  <script src="https://cdn.jsdelivr.net/npm/web3@1.10.0/dist/web3.min.js"></script>
</head>
<body>
  <button onclick="connectWallet()">Connect MetaMask</button>
  <p id="wallet-address"></p>

  <script>
    async function connectWallet() {
      if (window.ethereum) {
        try {
          const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
          document.getElementById('wallet-address').innerText = 'Connected: ' + accounts[0];
        } catch (err) {
          console.error('User rejected connection:', err);
        }
      } else {
        alert('MetaMask not found!');
      }
    }
  </script>
</body>
</html>
