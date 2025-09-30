// AutoU Email Classifier - JavaScript Functions

// Global variables
let loadingModal;
let successToast;
let errorToast;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeComponents();
    setupEventListeners();
});

function initializeComponents() {
    // Initialize Bootstrap components
    loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'), {
        keyboard: false,
        backdrop: 'static'
    });
    
    successToast = new bootstrap.Toast(document.getElementById('successToast'));
    errorToast = new bootstrap.Toast(document.getElementById('errorToast'));
}

function setupEventListeners() {
    // File form submission
    document.getElementById('fileForm').addEventListener('submit', function(e) {
        e.preventDefault();
        handleFileSubmission();
    });
    
    // Text form submission
    document.getElementById('textForm').addEventListener('submit', function(e) {
        e.preventDefault();
        handleTextSubmission();
    });
    
    // File input change
    document.getElementById('fileInput').addEventListener('change', function(e) {
        handleFileSelection(e.target.files[0]);
    });
    
    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        document.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
}

// Drag and drop handlers
function dragOverHandler(ev) {
    ev.preventDefault();
    ev.currentTarget.classList.add('drag-over');
}

function dragLeaveHandler(ev) {
    ev.preventDefault();
    ev.currentTarget.classList.remove('drag-over');
}

function dropHandler(ev) {
    ev.preventDefault();
    ev.currentTarget.classList.remove('drag-over');
    
    const files = ev.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelection(files[0]);
    }
}

function handleFileSelection(file) {
    if (!file) return;
    
    // Validate file type
    const allowedTypes = ['text/plain', 'application/pdf'];
    const allowedExtensions = ['.txt', '.pdf'];
    
    const isValidType = allowedTypes.includes(file.type) || 
                       allowedExtensions.some(ext => file.name.toLowerCase().endsWith(ext));
    
    if (!isValidType) {
        showError('Tipo de arquivo não permitido. Use apenas arquivos .txt ou .pdf');
        return;
    }
    
    // Validate file size (16MB max)
    const maxSize = 16 * 1024 * 1024; // 16MB
    if (file.size > maxSize) {
        showError('Arquivo muito grande. Tamanho máximo: 16MB');
        return;
    }
    
    // Update file info display
    document.getElementById('fileName').textContent = `${file.name} (${formatFileSize(file.size)})`;
    document.querySelector('.file-info').classList.remove('d-none');
    
    // Set file in input
    const fileInput = document.getElementById('fileInput');
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    fileInput.files = dataTransfer.files;
}

function handleFileSubmission() {
    const fileInput = document.getElementById('fileInput');
    
    if (!fileInput.files || fileInput.files.length === 0) {
        showError('Por favor, selecione um arquivo');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    submitToAPI(formData);
}

function handleTextSubmission() {
    const emailText = document.getElementById('emailText').value.trim();
    
    if (!emailText) {
        showError('Por favor, insira o texto do email');
        return;
    }
    
    if (emailText.length < 10) {
        showError('O texto deve ter pelo menos 10 caracteres');
        return;
    }
    
    const formData = new FormData();
    formData.append('email_text', emailText);
    
    submitToAPI(formData);
}

async function submitToAPI(formData) {
    try {
        // Show loading modal
        loadingModal.show();
        
        // Hide previous results
        document.getElementById('results').classList.add('d-none');
        
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Erro no servidor');
        }
        
        // Hide loading modal
        loadingModal.hide();
        
        // Display results
        displayResults(data);
        
        // Show success message
        showSuccess('Email analisado com sucesso!');
        
    } catch (error) {
        console.error('Error:', error);
        loadingModal.hide();
        showError(error.message || 'Erro ao processar o email');
    }
}

function displayResults(data) {
    // Update classification badge
    const classificationBadge = document.getElementById('classificationBadge');
    const classification = data.classification;
    
    classificationBadge.textContent = classification;
    classificationBadge.className = 'badge fs-6 px-3 py-2 ' + 
        (classification === 'PRODUTIVO' ? 'bg-success' : 'bg-secondary');
    
    // Update suggested response
    document.getElementById('suggestedResponse').textContent = data.suggested_response;
    
    // Update statistics
    document.getElementById('charCount').textContent = formatNumber(data.char_count || '0');
    document.getElementById('wordCount').textContent = formatNumber(data.word_count || '0');
    
    // Show results with animation
    const resultsDiv = document.getElementById('results');
    resultsDiv.classList.remove('d-none');
    resultsDiv.classList.add('fade-in-up');
    
    // Scroll to results
    setTimeout(() => {
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 300);
}

function clearFile() {
    document.getElementById('fileInput').value = '';
    document.querySelector('.file-info').classList.add('d-none');
}

function copyResponse() {
    const responseText = document.getElementById('suggestedResponse').textContent;
    
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(responseText).then(() => {
            showSuccess('Resposta copiada para a área de transferência!');
        }).catch(() => {
            fallbackCopyResponse(responseText);
        });
    } else {
        fallbackCopyResponse(responseText);
    }
}

function fallbackCopyResponse(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showSuccess('Resposta copiada para a área de transferência!');
    } catch (err) {
        showError('Não foi possível copiar. Selecione o texto manualmente.');
    }
    
    document.body.removeChild(textArea);
}

function analyzeAnother() {
    // Hide results
    document.getElementById('results').classList.add('d-none');
    
    // Clear forms
    document.getElementById('fileForm').reset();
    document.getElementById('textForm').reset();
    clearFile();
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function loadExample(type) {
    const examples = {
        'produtivo': `Prezados,

Estou enfrentando dificuldades para acessar o sistema corporativo desde ontem à tarde. Quando tento fazer login, recebo a mensagem de erro "Credenciais inválidas", mesmo tendo certeza de que estou usando a senha correta.

Este problema está impactando minha produtividade, pois preciso acessar os relatórios financeiros para a reunião de amanhã.

Poderiam me ajudar a resolver esta questão com urgência?

Aguardo retorno.

Atenciosamente,
João Silva
Departamento Financeiro`,

        'improdutivo': `Olá pessoal,

Espero que todos estejam bem!

Quero parabenizar toda a equipe pelo excelente trabalho realizado no último trimestre. Os resultados superaram nossas expectativas e isso só foi possível graças ao empenho de cada um.

Aproveito para desejar um ótimo final de semana para todos.

Abraços,
Maria Santos
Gerente de Projetos`
    };
    
    // Switch to text tab
    const textTab = document.getElementById('text-tab');
    const textTabPane = document.getElementById('text');
    
    // Activate text tab
    textTab.click();
    
    // Fill textarea with example
    setTimeout(() => {
        document.getElementById('emailText').value = examples[type];
        document.getElementById('emailText').focus();
        
        // Scroll to textarea
        document.getElementById('emailText').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
    }, 200);
}

function showSuccess(message) {
    document.getElementById('toastMessage').textContent = message;
    successToast.show();
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    errorToast.show();
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatNumber(num) {
    // Converter para número se for string
    const number = typeof num === 'string' ? parseInt(num) || 0 : num;
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

// Utility function to validate email format (if needed)
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Add smooth scrolling to all internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading states to buttons
function addLoadingState(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processando...';
    button.disabled = true;
    
    return function removeLoadingState() {
        button.innerHTML = originalText;
        button.disabled = false;
    };
}

// Performance monitoring
window.addEventListener('load', function() {
    if ('performance' in window && 'timing' in window.performance) {
        const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
        console.log(`Page loaded in ${loadTime}ms`);
    }
});

// Service Worker registration (for PWA features if needed)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Commented out - uncomment if you want PWA features
        // navigator.serviceWorker.register('/sw.js').then(function(registration) {
        //     console.log('ServiceWorker registration successful');
        // }).catch(function(err) {
        //     console.log('ServiceWorker registration failed');
        // });
    });
}