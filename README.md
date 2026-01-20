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

| Atributo | Função   |
|----------|----------|
| loadImages   | carrega todas as imagens|
| loadAnimations  | carrega todas as imagens|

#### Uso

##### Inicializando
Antes de carregar o jogo use ```loadImages()``` e ```loadAnimations()```.

#### Adicionando nova imagem
Caso queira carregar uma nova imagem no jogo, adicione a imagem na pasta Assets->Images e procure a pasta apropriada, em seguida vá ao método ```loadImages()``` e coloque```Assets["um nome legal para sua imagem"]= pygame.image.load("caminho_da_imagem + nome_da_imagem").convert_alpha()```.

##### Acesso
Caso queira acessar a imagem em qualquer lugar do código lembre-se de importar a classe e use ```Assets.images["nome"]```, o mesmo vale para animações.

### Classe Screen
#### Local
HellPatrol->screen.py



