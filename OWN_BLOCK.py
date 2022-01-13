from flask import Flask, jsonify
import hashlib
import datetime
import json

# creo clase blockchain
class Blockchain:
    # defino el constructor y como de primeras creo un array que contiene la CADENAD E BLOQUES, cada indice es cada bloque, que cada bloque es un diccionario con clave valor mas aabajo.
    def __init__(self):

        self.chain = []
        #creo el primer bloque, proof=1, previous hash = 0 ya que es el primero.
        self.create_block(proof=1, previous_hash='0')

    # defino una funcion para crear un bloque, argumentos proof y prev hash para ir anidando bloques.
    def create_block(self, proof, previous_hash):
        #creo un diccionario con clave valor correspondiente.
        new_block = {
            'number':len(self.chain)+1,
            'previous_hash':previous_hash,
            'timestamp':str(datetime.datetime.now()),
            'proof': proof
        }
        # agrego el diccionario anterior a la cadena de bloques o array.
        self.chain.append(new_block)
        return new_block
    
    # imprimir el ultimo bloque
    def print_last_block(self):

        return self.chain[-1]

    # Prueba de trabajo
    def proof_of_work(self, previous_proof):
        new_proof = 1
        is_okay = False

        while is_okay is False:
            final_hash = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()

            # si los primeros 4 digitos son igual a lo que yo puse, 4 ceros
            if final_hash[:4] == '0000':
                is_okay = True
            else:   
                new_proof += 1
            
        return new_proof
    
    # sacar valor hash de un bloque
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True, separators=('.', '=')).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    # validador de cadenas de bloques
    def chain_validator(self, chain):
        #iniciamos con el bloque numero 0
        previous_block = chain[0]
        # iniciamos un indicde que es +1 al inicial.
        block_index = 1

        # un while mientras index sea menor a la longitud ,  -1, ya que siempre necesitamos -1 bloque para comprobar el siguiente con el hash actual y previous hash.
        while block_index < len(chain):

            # definimos un nuevo bloque con la posicion de indice actual
            block = chain[block_index]
            # si el previous hash del bloque actual es distinto al hash del bloque anterior con la funcion sacar valor hash, retornamos falso, ya que no son iguales.
            if (block['previous_hash'] != self.hash(previous_block)):
                return False
            
            # previous_block le otorgamos el valor del proof de previous_block
            previous_block = previous_block['proof']
            # creamos una nueva prueba un unevo proof otorgandole el proof edl block
            proof = block['proof']

            # con los valores anteriores creamos un hash
            # sigo sin entender por qué proof y previous block al cuadrado.
            hash_operation = hashlib.sha256(str(proof**2-previous_block**2).encode()).hexdigest()

            # si los primeros 4 digitos del hash anterior son distintos al proof de 4 ceros return false.
            if hash_operation[:4] != '0000':
                return False

            # cambiamos de bloque, ahora, pasamos al de adelante, previous = block, block_index + 1.
            previous_block = block
            block_index += 1
        
        # si todo salio bien, true.
        return True

# creo una app de flask.
app = Flask(__name__)
# creo una instancia de blockchain.
blockchain = Blockchain()

# creamos la mineria ed bloques
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.print_last_block()
    previous_proof = previous_block['proof']
    previous_hash = blockchain.hash(previous_block)
    proof = blockchain.proof_of_work(previous_proof)
    new_block = blockchain.create_block(proof, previous_hash)
    new_hash = blockchain.hash(new_block)

    response = {
        'msg':'Congratulations! Block mined!',
        'status':'200',
        'timestamp':new_block['timestamp'],
        'previous_hash': new_block['previous_hash'],
        'block_hash':new_hash
    }

    return jsonify(response), 200

# creamos la obtencion de la blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    chain = blockchain.chain
    response = {
        'chain':chain,
        'length_chain': len(chain)
    }

    return jsonify(response), 200

# creamos la validacion  de la chain.
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_validator(blockchain.chain)

    if valid:
        response = {'status':'1', 'msg':'blockchain works.'}
    else:
        response = {'status':'0', 'msg':'blockchain dont work.'}
    
    return jsonify(response), 200

app.run(host='0.0.0.0', port=5000)
