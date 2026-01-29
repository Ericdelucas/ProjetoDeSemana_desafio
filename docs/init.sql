CREATE DATABASE IF NOT EXISTS smartsaude CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE smartsaude;

CREATE TABLE IF NOT EXISTS unidades (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(180) NOT NULL,
  endereco VARCHAR(255) NOT NULL,
  lat DOUBLE NOT NULL,
  lng DOUBLE NOT NULL,
  medicos_ativos INT NOT NULL DEFAULT 1,
  pacientes_fila INT NOT NULL DEFAULT 0,
  tipo ENUM('UPA','UBS','Hosp') NOT NULL,
  INDEX idx_unidades_lat_lng (lat, lng)
);

CREATE TABLE IF NOT EXISTS estoque (
  id INT AUTO_INCREMENT PRIMARY KEY,
  unidade_id INT NOT NULL,
  medicamento_nome VARCHAR(180) NOT NULL,
  categoria VARCHAR(120) NOT NULL,
  qtd_status ENUM('Disponível','Crítico','Indisponível') NOT NULL DEFAULT 'Disponível',
  INDEX idx_estoque_unidade_categoria (unidade_id, categoria),
  INDEX idx_estoque_medicamento (medicamento_nome),
  CONSTRAINT fk_estoque_unidade FOREIGN KEY (unidade_id) REFERENCES unidades(id)
);

INSERT INTO unidades (nome,endereco,lat,lng,medicos_ativos,pacientes_fila,tipo) VALUES
('UPA Central','Rua A, 100', -23.5505, -46.6333, 6, 40,'UPA'),
('UBS Jardim','Rua B, 200', -23.5590, -46.6400, 3, 18,'UBS'),
('Hospital Municipal','Av C, 300', -23.5450, -46.6200, 12, 90,'Hosp');

INSERT INTO estoque (unidade_id, medicamento_nome, categoria, qtd_status) VALUES
(1,'Dipirona 500mg','Analgésico','Disponível'),
(1,'Amoxicilina 500mg','Antibiótico','Crítico'),
(2,'Soro Fisiológico 0,9%','Insumo','Disponível'),
(3,'Insulina NPH','Endócrino','Indisponível');
