/**
 *  ESTE SERVIDOR ERA ANTIGO, UTILIZADO PARA TESTE E VISUALIZAÇÃO DE BANCO DE DADOS
 * A IMPLEMENTAÇÃO ESTÁ OCORRENDO NO server.py
 */
const express = require('express');
const { MongoClient } = require('mongodb');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;
const url = 'mongodb://localhost:27017';
const dbName = 'diagnostico_db'; // Nosso banco de dados principal
const client = new MongoClient(url);

app.use(bodyParser.urlencoded({ extended: true }));

async function main() {
    await client.connect();
    console.log('[Servidor] Conectado com sucesso ao servidor MongoDB');
    const db = client.db(dbName);

    // Preparando as duas coleções que vamos usar
    const collectionTremor = db.collection('leituras_tremor');
    const collectionSaliva = db.collection('amostras_saliva');

    // ROTA #1: Para receber os dados do MPU-6050
    
    app.post('/tremor', async (req, res) => {
        const { frequencia } = req.body;

        if (frequencia === undefined) {
            return res.status(400).send('Erro: campo "frequencia" não encontrado.');
        }

        console.log(`[Servidor] Leitura de TREMOR recebida: ${frequencia} Hz`);
        
        const novoDadoTremor = {
            frequencia: parseFloat(frequencia),
            timestamp: new Date()
        };

        await collectionTremor.insertOne(novoDadoTremor);
        res.status(200).send('Dado de tremor recebido e salvo com sucesso');
    });

    // ROTA #2: Para receber os dados do TCS34725
    
    app.post('/saliva', async (req, res) => {
        const { r, g, b, c, corDetectada } = req.body;

        if (r === undefined || g === undefined || b === undefined) {
            return res.status(400).send('Erro: dados de cor incompletos.');
        }

        console.log(`[Servidor] Amostra de SALIVA recebida: R=${r}, G=${g}, B=${b}, Cor=${corDetectada}`);
        
        const novaAmostra = {
            valoresRGB: { r: parseInt(r), g: parseInt(g), b: parseInt(b), c: parseInt(c) },
            corDetectada: corDetectada,
            timestamp: new Date()
        };

        await collectionSaliva.insertOne(novaAmostra);
        res.status(200).send('Amostra de saliva recebida e salva com sucesso');
    });

    app.listen(port, () => {
        console.log(`[Servidor] Rodando e ouvindo em http://localhost:${port}`);
        console.log('[Servidor] Endpoints ativos: /tremor, /saliva');
    });
}

main().catch(console.error);