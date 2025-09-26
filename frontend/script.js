
const API_URL = 'http://localhost:5000';

// Função para atualizar o painel de Tremor
async function atualizarDadosTremor() {
    try {
        const response = await fetch(`${API_URL}/api/tremores_data`);
        const dados = await response.json();

        const corpoTabela = document.getElementById('dados-tremor');
        corpoTabela.innerHTML = ''; // Limpa a tabela

        if (dados.length === 0) {
            corpoTabela.innerHTML = '<tr><td colspan="3">Aguardando dados do sensor de tremor...</td></tr>';
            return;
        }

        // Atualiza o diagnóstico principal com o dado mais recente
        const maisRecente = dados[0];
        const textoDiagnostico = document.getElementById('diagnostico-texto');
        const confiancaDiagnostico = document.getElementById('diagnostico-confianca');
        
        textoDiagnostico.textContent = maisRecente.diagnostico || 'N/A';
        confiancaDiagnostico.textContent = `${maisRecente.confianca || '--%'}`;
        textoDiagnostico.className = (maisRecente.diagnostico && (maisRecente.diagnostico.toLowerCase().includes('anormal') || maisRecente.diagnostico.toLowerCase().includes('positivo'))) ? 'status-anormal' : 'status-normal';

        // Preenche a tabela com o histórico
        dados.forEach(leitura => {
            const linha = `
                <tr>
                    <td>${new Date(leitura.timestamp).toLocaleTimeString()}</td>
                    <td>${leitura.frequencia.toFixed(2)} Hz</td>
                    <td>${leitura.diagnostico || 'N/A'}</td>
                </tr>
            `;
            corpoTabela.innerHTML += linha;
        });

    } catch (error) {
        console.error('Erro ao buscar dados de tremor:', error);
    }
}

// Função para atualizar o painel de Saliva
// Localizado em: frontend/script.js

async function atualizarDadosSaliva() {
    try {
        const response = await fetch(`${API_URL}/api/saliva_data`);
        const dados = await response.json();

        const corpoTabela = document.getElementById('dados-saliva');
        corpoTabela.innerHTML = '';

        if (dados.length === 0) {
            corpoTabela.innerHTML = '<tr><td colspan="4">Aguardando dados do sensor de saliva...</td></tr>';
            return;
        }

        const maisRecente = dados[0];
        document.getElementById('cor-detectada').textContent = `Cor: ${maisRecente.analysisResult}`;
        const swatch = document.getElementById('cor-swatch');
        
        // =================================================================
        // --- BLOCO DE DEBUG ---
        // =================================================================
        const raw_r = maisRecente.readings.r;
        const raw_g = maisRecente.readings.g;
        const raw_b = maisRecente.readings.b;

        // Imprime os valores brutos que vieram do sensor
        console.log("Valores Brutos do Sensor (R,G,B):", raw_r, raw_g, raw_b);

        //Foi ajustado o divisor.
        const divisor = 25; 
        
        // Calcula os valores para o CSS
        const r_css = Math.round(Math.min(255, raw_r / divisor));
        const g_css = Math.round(Math.min(255, raw_g / divisor));
        const b_css = Math.round(Math.min(255, raw_b / divisor));

        // Imprime os valores que serão usados para colorir a bolinha
        console.log("Valores Calculados para o CSS (R,G,B):", r_css, g_css, b_css);
        // =================================================================

        swatch.style.backgroundColor = `rgb(${r_css}, ${g_css}, ${b_css})`;

        // Preenche a tabela com o histórico (código sem alteração)
        dados.forEach(analise => {
            // ... (o resto da função continua igual)
            const r_val = analise.readings.r;
            const g_val = analise.readings.g;
            const b_val = analise.readings.b;
            const linha = `
                <tr>
                    <td>${new Date(analise.timestamp).toLocaleTimeString()}</td>
                    <td>${analise.analysisResult}</td>
                    <td>${r_val}, ${g_val}, ${b_val}</td>
                    <td>${analise.readings.lux}</td>
                </tr>
            `;
            corpoTabela.innerHTML += linha;
        });

    } catch (error) {
        console.error('Erro ao buscar dados de saliva:', error);
    }
}

// Inicia o processo de atualização quando a página carrega
document.addEventListener('DOMContentLoaded', () => {
    atualizarDadosTremor();
    atualizarDadosSaliva();
    setInterval(() => {
        atualizarDadosTremor();
        atualizarDadosSaliva();
    }, 3000); // Atualiza tudo a cada 3 segundos
});