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

        // Atualiza o display principal com o dado mais recente
        const maisRecente = dados[0];
        document.getElementById('cor-detectada').textContent = `Cor: ${maisRecente.analysisResult}`;
        const swatch = document.getElementById('cor-swatch');
        // Normaliza os valores de R,G,B para o CSS (que usa 0-255)
        const r = Math.min(255, maisRecente.readings.r / 20); // Ajuste o divisor conforme a sensibilidade
        const g = Math.min(255, maisRecente.readings.g / 20);
        const b = Math.min(255, maisRecente.readings.b / 20);
        swatch.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;

        // Preenche a tabela com o histórico
        dados.forEach(analise => {
            const r = analise.readings.r;
            const g = analise.readings.g;
            const b = analise.readings.b;
            const linha = `
                <tr>
                    <td>${new Date(analise.timestamp).toLocaleTimeString()}</td>
                    <td>${analise.analysisResult}</td>
                    <td>${r}, ${g}, ${b}</td>
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