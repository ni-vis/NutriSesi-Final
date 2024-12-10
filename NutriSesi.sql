CREATE DATABASE NutriSesi;

USE NutriSesi;

-- Criação da tabela Bebida
CREATE TABLE Bebida (
    idBebida INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(60) NOT NULL
);

-- Criação da tabela Salada
CREATE TABLE Salada (
    idSalada INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(60) NOT NULL
);

-- Criação da tabela Sobremesa
CREATE TABLE Sobremesa (
    idSobremesa INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(60) NOT NULL
);

-- Criação da tabela Prato_principal
CREATE TABLE Prato_principal (
    idPrato_principal INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(60) NOT NULL
);

-- Criação da tabela Categoriacardapio
CREATE TABLE Categoria (
    idCategoria INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(60) NOT NULL
);

-- Criação da tabela Cardapio
CREATE TABLE Cardapio (
    idCardapio INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL,
    idBebida INT,
    idSobremesa INT NOT NULL,
    idPrato_principal INT NOT NULL,
    idSalada INT,
    idCategoria INT NOT NULL,
    FOREIGN KEY (idBebida) REFERENCES Bebida(idBebida),
    FOREIGN KEY (idSobremesa) REFERENCES Sobremesa(idSobremesa),
    FOREIGN KEY (idPrato_principal) REFERENCES Prato_principal(idPrato_principal),
    FOREIGN KEY (idSalada) REFERENCES Salada(idSalada),
    FOREIGN KEY (idCategoria) REFERENCES Categoria(idCategoria)
);

-- Criação da tabela Feedback
CREATE TABLE Feedback (
    idFeedback INT AUTO_INCREMENT PRIMARY KEY,
    aprovacao TINYINT NOT NULL,
    comentario TEXT,
    data_feedback TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    idCardapio INT,
    FOREIGN KEY (idCardapio) REFERENCES Cardapio(idCardapio)
);

ALTER TABLE feedback
ADD CONSTRAINT fk_cardapio
FOREIGN KEY (idCardapio)
REFERENCES cardapio(idCardapio)
ON DELETE CASCADE;

