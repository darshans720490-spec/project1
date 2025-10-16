document.addEventListener('DOMContentLoaded', function() {
    // Salary calculation for generate slip form
    const basicSalaryInput = document.getElementById('basic_salary');
    const allowancesInput = document.getElementById('allowances');
    const deductionsInput = document.getElementById('deductions');
    const grossSalarySpan = document.getElementById('gross-salary');
    const netSalarySpan = document.getElementById('net-salary');

    function calculateSalary() {
        if (basicSalaryInput && allowancesInput && deductionsInput) {
            const basicSalary = parseFloat(basicSalaryInput.value) || 0;
            const allowances = parseFloat(allowancesInput.value) || 0;
            const deductions = parseFloat(deductionsInput.value) || 0;
            
            const grossSalary = basicSalary + allowances;
            const netSalary = grossSalary - deductions;
            
            if (grossSalarySpan) grossSalarySpan.textContent = grossSalary.toFixed(2);
            if (netSalarySpan) netSalarySpan.textContent = netSalary.toFixed(2);
        }
    }

    // Add event listeners for salary calculation
    if (basicSalaryInput) basicSalaryInput.addEventListener('input', calculateSalary);
    if (allowancesInput) allowancesInput.addEventListener('input', calculateSalary);
    if (deductionsInput) deductionsInput.addEventListener('input', calculateSalary);

    // Initial calculation
    calculateSalary();

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#dc3545';
                } else {
                    field.style.borderColor = '#ced4da';
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // Table row highlighting
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#f8f9fa';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });

    // Auto-set current month and year
    const monthSelect = document.getElementById('month');
    const yearInput = document.getElementById('year');
    
    if (monthSelect && yearInput) {
        const now = new Date();
        const currentMonth = now.toLocaleString('default', { month: 'long' });
        const currentYear = now.getFullYear();
        
        // Set current month as default
        for (let option of monthSelect.options) {
            if (option.value === currentMonth) {
                option.selected = true;
                break;
            }
        }
        
        // Set current year as default
        yearInput.value = currentYear;
    }

    // Confirm before generating slip
    const generateSlipForms = document.querySelectorAll('form[action*="create_slip"]');
    generateSlipForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const employeeName = document.querySelector('.employee-info p strong').nextSibling.textContent.trim();
            const month = document.getElementById('month').value;
            const year = document.getElementById('year').value;
            
            if (!confirm(`Generate salary slip for ${employeeName} for ${month} ${year}?`)) {
                e.preventDefault();
            }
        });
    });
});