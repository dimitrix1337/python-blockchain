import pprint
import json
import hashlib
from datetime import datetime
from time import time

# Defino la clase bloque
class Block:

    # inicializador, timestamp, transacciones o datos, bloque previo
    def __init__(self, timestamp, trans, previous_block='' ):
        self.timestamp = timestamp
        self.trans = trans
        self.previous_block = previous_block
        # dificultad
        self.moreHarder = 0
        # hash propio del bloque actual, lo calculamos con calculateHash
        self.hash = self.calculateHash(trans,timestamp, self.moreHarder)
    
    # funcion para calcular hash con 3 argumentos
    def calculateHash(self, trans, timestamp, moreHarder):
        # simplemente organizamos los 3 argumentos en 1 como strings, luego codificamos a utf-8
        data = str(trans) + str(timestamp) + str(moreHarder)
        data = data.encode()
        #calculamos el hash del data encoded, luego lo pasamos a hexadecimal
        hash = hashlib.sha256(data).hexdigest()
        return hash
    
    # funcion para minar bloques, recibe como argumento la dificultad actual
    def mined_block(self, difficulty):
        # difficultyCheck es simplemente los 0 que quiero que tenga el hash al inicio para ser valido,
        # el 0 se multiplica tantas veces como sea la dificultad, ejemplo: difficulty = 5, -> 00000
        difficultyCheck = "0" * difficulty
        # si los primeros digitos del hash actual (demarcado por difficulty) es distinto a lo que pido, sigo minando, hasta obtenerlo
        while self.hash[:difficulty] != difficultyCheck:
            # calculo un nuevo hash
            self.hash = self.calculateHash(self.trans, self.timestamp, self.moreHarder)
            # aumento dificultad en 1
            self.moreHarder += 1

# creo clase blockchain
class Blockchain:

    #inicializador
    def __init__(self):
        # creo el array que contendrá todos los bloques anidados, este empieza con el Genesis Block (bloque 0, o bloque inicial)
        self.chain = [self.GenesisBlock()]
        # array de transacciones pendientes de la mempool
        self.pendingTransactions = []
        # recompensa por minar bloque para mineros, numero adimensional
        self.reward = 50
        # difficultad inicial de la blockchain, '000' 3 ceros.
        self.difficulty = 3
        # revoluciones para el halving, inicia en 1
        self.t = 1
    
    # crear halving
    def halving(self):
        # si la longitud de la cadena >=210000*revoluciones
        if (len(self.chain)>=(2*self.t)):
            # aumentamos revolucion + 1
            self.t += 1
            # dividimos la recompensa entre 2
            self.reward = self.reward / 2
            # aumentamos + 1 la dificultad
            self.difficulty += 1
        
    # funcion del Genesis block ,bloque inicial
    def GenesisBlock(self):
        # creamos una instancia llamada gensisBlock derivada de Block creada anteriormente, le pasamos los parametros del constructor
        genesisBlock = Block(datetime.now(), 'First Block')
        return genesisBlock
    # getter del ultimo bloque
    def GetLastBlock(self):
        return self.chain[-1]
    
    def minePending(self, minerRewardAddress, number=0):
        print('Reward antes del halving: ', self.reward)
        self.halving()
        print('Reward despues del halving: ', self.reward)
        newBlock = Block(str(datetime.now()), self.pendingTransactions)
        newBlock.mined_block(self.difficulty)
        newBlock.previous_block = self.GetLastBlock().hash

        print(f"Hash del bloque prev: {newBlock.previous_block}")

        testChain = []
        for trans in newBlock.trans:
            temp = json.dumps(trans.__dict__, indent=5, separators=(',', ':'))
            testChain.append(temp)
        pprint.pprint(testChain)

        self.chain.append(newBlock)
        print(f'Hash del bloque: {newBlock.hash}')
        print('Bloque añadido.')

        rewardTrans = Transaction("- RECOMPENSADO:", minerRewardAddress, self.reward)
        self.pendingTransactions.append(rewardTrans)
        self.pendingTransactions = []

    def valid_chain(self):
        for i in range(1,len(self.chain)):

            currentBlock = self.chain[i]
            previousBlock = self.chain[i-1]

            if currentBlock.previous_block != previousBlock.hash:
                print(f'INvalid chain, different hash block {i} with {i-1} Next block previous hash: {currentBlock.previous_block} - Previous block hash: {previousBlock.hash}')
        print('The chain is valid and secure.')

    def add_transaction(self, transaction):
        self.pendingTransactions.append(transaction)
    
    def getBalance(self, walletAddress):

        balance = 0

        for block in self.chain:
            if block.previous_block=="":
                continue
            for transaction in block.trans:
                if transaction.FromWallet == walletAddress:
                    balance -= transaction.amount
                if transaction.ToWallet == walletAddress:
                    balance += transaction.amount
        return balance

class Transaction:
    def __init__(self, FromWallet, ToWallet, amount):
        self.FromWallet = FromWallet
        self.ToWallet = ToWallet
        self.amount = amount

criptopay = Blockchain()
print('Octavio empeoz a minar...')
criptopay.add_transaction(Transaction('0x9938409si9391', '0x123jjkr78371', 0.05))
criptopay.add_transaction(Transaction('0x784918473713', '0x554818jd88e1', 0.99))
criptopay.add_transaction(Transaction('0x784918473713', '0x554818jd88e1', 0.29))
criptopay.minePending("Octavius")
criptopay.add_transaction(Transaction('0x9938409si9391', '0x123jjkr78371', 0.75))
criptopay.add_transaction(Transaction('0x784918473713', '0x554818jd88e1', 0.88))
criptopay.add_transaction(Transaction('0x9938409si9391', '0x123jjkr78371', 0.11))
criptopay.minePending("Octavius")
criptopay.add_transaction(Transaction('0x784918473713', '0x554818jd88e1', 99))
criptopay.add_transaction(Transaction('0x9938409si9391', '0x123jjkr78371', 105))
criptopay.minePending("Octavius")



print(f'El minero octavio recaudó por minar: {criptopay.getBalance("Octavius")} Bitcoins.')

