# Hell-Patrol-Project
Jogo para a atividade de socket da matéria de Desenvolvimento de Sistemas Distribuídos
## Classes do projeto
### Classe Assets
#### Local
Vá na pasta HellPatrol->Assets->assets.py

#### Função 

Essa classe tem como função principal principal carregar todas as imagens e animações que serão usadas no jogo. Se não o fizessemos, a cada frame seria necessário buscar os arquivos que estão na memória do disco, dessa forma o jogo travaria a todo momento.

#### Atributos

| Atributo | Função   |
|----------|----------|
| images   | Dicionário que guarda imagens e tem como chave os seus respectivos nomes|
| animations  | Dicionário que guarda animações(Animações são tratadas apenas como uma lista de imagens) e tem como chave os seus respectivos nomes|

#### Métodos

| Método | Função   |
|----------|----------|
| loadImages   | carrega todas as imagens|
| loadAnimations  | carrega todas as imagens|

#### Uso

##### Inicializando
A classe possui todos os métodos e atributos com estáticos, ou seja não tente instancia-la. Antes de carregar o jogo use ```loadImages()``` e ```loadAnimations()```.

#### Adicionando nova imagem
Caso queira carregar uma nova imagem no jogo, adicione a imagem na pasta Assets->Images e procure a pasta apropriada, em seguida vá ao método ```loadImages()``` e coloque```Assets["um nome legal para sua imagem"]= pygame.image.load("caminho_da_imagem + nome_da_imagem").convert_alpha()```.

##### Acesso
Caso queira acessar a imagem em qualquer lugar do código lembre-se de importar a classe e use ```Assets.images["nome"]```, o mesmo vale para animações.

### Classe Screen
#### Local
HellPatrol->screen.py

#### Função
Tem como função inicializar o display, desenhar imagens na tela e gerenciar a câmera

#### Atributos
| Atributo | Função   |
|----------|----------|
| screen   | Display|
| screenWidth | largura da tela|
| screenHeight | altura da tela|
| camera | tupla que contém a posição da camera|

#### Métodos
| Método | Função   |
|----------|----------|
| updateCamera(newPosX,newPosY)|Atualiza a posição da camera|
| updateScreen(newPosX,newPosY)|Atualiza a tela apagando todos os elementos e preparando-a para o próximo frame|
| drawBackground(tileMap) | Desenha o tileMap|
| drawSprite(sprite,posX,posY,rotation) | Desenha uma imagem no local e com a rotação indicada|
| drawAimLine(direction,playerx,playery) | Desenha a linha de mira que sai da arma do player|
| drawReticle() | Desenha a mira do player|

#### Uso

#### Inicializando

Instancie dando a posição em X e em Y que é onde o player vai spawnar. Exemplo:
```screen=Screen(80,80)```

### Classe Entity

#### Local
HellPatrol->Entities->entity.py

#### Função
Essa classe é uma classe abstrata, pelo que pesquisei não tem como criar classes abstratas em python, apenas métodos abstratos(Vai saber porque), se você for ver a definição dela vai perceber que você pode instanciar objetos com ela mas NUNCA faça isso, a única função dela é servir como molde para outras classe. Basicamente essa classe vai conter atributos e métodos que serão compartilhadas por todos os objetos que estão no jogo como: Posição, largura, altura, imagem, Caixa de colisão, rotação e tipo.

#### Atributos 

| Atributo | Função   |
|----------|----------|
| width   | Largura do objeto|
| height | Altura do objeto|
| collider | Caixa de colisão do objeto|
| x | Posição no eixo X|
| y | Posição no eixo Y|
| direction | Vector que representa a rotação do objeto|
| images | Lista com as imagens que o objeto que vai exibir na tela, a ordem dos objetos nessa lista influência na profundidade|
| type | Tag/Tipo do objeto|
| dead | Booleano que indica se o objeto deve ser removido na proxíma atualização|

#### Métodos 

| Método | Função   |
|----------|----------|
| update(dt)|Método abstrato. É chamado pelo obeto a cada frame|
| adjustImage()|Método abstrato. Serve para alterar a imagem do objeto|
| getImages() | retorna o atributo images|
| drawCollider(self,tela,camera) | Desenha a caixxa de colisão do objeto|
| getRotation() | Retorna a rotação em graus do objeto|

#### Uso
Como já disse antes essa é apenas uma classe abstrata servindo apenas para ser herdada por outras classes. Caso você queira uma classe com objetos estáticos, como uma parede, herde essa classe diretamente, caso você queira uma classe com objetos dinâmicos que mudam de posição e estado constantemente herde a classe ```Mob``` que será abordada a seguir.

### Classe Mob(Entity)
#### Local
HellPatrol->Entities->Mob->mob.py

#### Função
Essa é um classe abstrata que herda a classe Entity, servindo para gerar classes que possuam objetos dinâmicos como balas, inimigos e o próprio jogador.
> ⚠️ **Aviso:** Para um entendimento completo dessa classe é importante ter conhecimento da classe StateMachine e States.


#### Atributos

| Atributo | Função   |
|----------|----------|
| vel  |Velocidade do objeto|
| states | Lista de StateMachine do objeto|
| entities | Referência para a lista que contém todos os objetos do jogo como: Inimigos, Balas e etc|

#### Métodos


| Método | Função   |
|----------|----------|
| update(dt) |Chamado a cada atualização de frame, ele faz com que todas statesMachines do objeto rodem o update do estado atual|
| move(dt) | Move o objeto de acordo com sua velocidade e direção|
| move2(dt) | Método auxiliar chamado pelo método move|

#### Uso

Como dito anteriormente use para gerar classes que tenham objetos dinâmicos no mundo, ou seja com mudança de estado e movimentação.

#### Player(Mob)
#### Local
HellPatrol->Entities->Mob->Player->player.py

#### Função

Herda a classe Mob.Basicamente, serve para criar o objeto que representa o player no jogo
> ⚠️ **Aviso:** Para um entendimento completo dessa classe é importante ter conhecimento da classe StateMachine,State,Animation,ControlAnimation e Weapon.

> ⚠️ **Aviso:** Vá para HellPatrol->Entities->Mob->Player->PlayerStates e veja lá os possíveis estados dessa classe.

#### Atributos


| Atributo | Função   |
|----------|----------|
| arsenal  |Lista com as possíveis armas do jogador|
| actualWeapon | Índice da arma atual do jogador|
| aimdirection | Vector que representa a direção para onde o jogado está mirando|
| animationmovimentb | Animação referente a corpo do jogador|
| animationcombat | Animação referente a arma do jogador|
| animationmovimenth | Animação referente a cabeça do jogador|
| screen | Referência para um objeto da classe Screen|
| switchweapontime | Animação referente a cabeça do jogador|

#### Métodos

| Método | Função   |
|----------|----------|
| attack() |Dispara com a arma atual|
| adjustImages() | Ajusta as imagens da lista de imagens de acordo com a animação atual|
| adjustAim() | Retorna a direção onde o jogador está mirando|
| switchWeapon() | Troca a arma do jogador|
| updateSwitchWeaponTime(dt) | Atualiza o tempo de espera para trocar a arma|
| canSwitch() | Retorna um booleano que indica se pode trocar a arma|
| canAttack(self) | Retorna um booleano que indica se pode atirar |
| isAttacking(self) | Retorna um booleano que indica se o jogador está atirando|
| getActualWeapon(self) | Retorna a arma atual que o jogador está usando|
| updateArsenal(self,dt) | Chama a função update nas armas do jogador|

### Classe StateMachine

#### Local
HellPatrol->Entities->Mob->StateMachine->stateMachine.py

#### Função
Armazena um conjunto de estados exclusivos entre si. Exemplo: Parado/Andando, EmCombate/NãoEstáEmCombate 

> ⚠️ **Aviso:** Confira a classe State.

#### Atributos

| Atributo | Função   |
|----------|----------|
| states | Dicionário que tem como valores estados e como chave os seus respectivos nomes|
| currentState |Estado Atual|

#### Métodos

| Método | Função   |
|----------|----------|
| switchTo(name) | troca o ```currentState``` para o estado que possui essa chave em ```states```|

### State

#### Local
HellPatrol->Entities->Mob->StateMachine->States->state.py

#### Função
Classe abstrata que serve para gerar estados de objetos.

> ⚠️ **Aviso:** Confira a classe StateMachine.

#### Atributos

| Atributo | Função   |
|----------|----------|
| stateName| Nome do estado|
| objRef | Referência do objeto que possui esse estado|

#### Métodos

| Método | Função   |
|----------|----------|
| entry | Ação que o estado realiza assim que é colocado como o atual na stateMachine|
| update | Ação que o estado realiza todo o frame|
| quit | Ação que o estado realiza assim que sai como o atual na stateMachine|

### ControlAnimation

#### Local
HellPatrol->Entities->ControlAnimation->controlanimation.py

#### Função
Classe que serve para armazenar animations exclusivos entre si.

> ⚠️ **Aviso:** Confira a classe Animation.

#### Atributos

| Atributo | Função   |
|----------|----------|
| animations | Dicionário que tem como valores animações e como chave os seus respectivos nomes|
| current |animação Atual|

#### Métodos

| Método | Função   |
|----------|----------|
| switchTo(name) | troca o ```current``` para a animação que possui essa chave em ```animations```|
| playCurrent(dt) | toca a animação de ```current```|
| currentImage() | retorna a imagem atual da animação em ```current```|

### Animation

#### Local
HellPatrol->Entities->ControlAnimation->Animation->animation.py

#### Função
Guarda um conjunto de imagens que compõe uma animação

#### Atributos

#### Atributos

| Atributo | Função   |
|----------|----------|
| animation | Conjunto de imagens da animação|
| name |nome da animação|
| speed |velocidade da animação|
| currentframe |frame atual da animação|
| framesINdex |número do frame da animação Atual|
| wait |tempo para mudar de um frame para outro|

#### Métodos

| Método | Função   |
|----------|----------|
| play(dt) | toca a animação|
| reset | reseta o ```waittime```|



























