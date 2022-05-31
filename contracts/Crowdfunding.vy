# @version ^0.2.0
# Plataforma de Crowdfunding v0.0.1

# Struct de dados do usuário
struct Donation:
  amount: uint256 # total doado

# Dicionário de usuários
donations: public(HashMap[address, Donation])

# Endereço do dono da vaquinha
owner: address

# Meta da vaquinha
target: public(uint256)

# Timestamp do fim da vaquinha
deadline: public(uint256)

# Função que inicializa o contrato
@external
def __init__(target: uint256, deadline: uint256):
  # Verifica que o deadline ainda não passou
  assert block.timestamp < deadline
  self.owner = msg.sender
  self.target = target
  self.deadline = deadline

# Função para que o dono encerre a vaquinha
@external
def finish():
  # Verifica que é o dono chamando a função
  assert msg.sender == self.owner
  assert block.timestamp >= self.deadline
  assert self.balance >= self.target

  send(msg.sender, self.balance)

# Função para que um usuário possa doar para a vaquinha
@external
@payable
def donate():
  # Verifica que a vaquinha ainda está aberta
  assert block.timestamp < self.deadline

  self.donations[msg.sender].amount += msg.value

# Função para que um usuário retire sua doação
@external
def withdraw():
  # Verifica que o usuário realmente doou alguma vez
  assert block.timestamp < self.deadline
  assert self.donations[msg.sender].amount > 0

  send(msg.sender, self.donations[msg.sender].amount)
  self.donations[msg.sender].amount = 0
