class Table {
    constructor(tableSection) {
        this.table = tableSection.querySelector('table');
        this.tableHeader = tableSection.querySelector('thead');
        this.tableBody = tableSection.querySelector('tbody');
        this.sortableColumns = tableSection.querySelectorAll('.sortable');
        this.searchInput = tableSection.querySelector('.search-input');
        this.resetBtn = tableSection.querySelector('.reset-btn');
        this.totalRecords = tableSection?.querySelector('.total-records');

        this.apiEndpoint = tableSection.dataset.endpoint;
        this.linkEndpoint = tableSection.dataset.link;
        this.params = tableSection.dataset.params;
        this.placeholder = tableSection.dataset.placeholder;
        this.actions = JSON.parse(tableSection.dataset.actions || '[]');
        this.columnKeys = this.getColumnKeys();
        this.colSpan = this.columnKeys.length + (this.actions.length || 0);

        this.allIds = JSON.parse(tableSection.dataset.allIds || '[]');
        this.allPlaceholders = JSON.parse(tableSection.dataset.allPlaceholders || '[]');
        this.allParams = JSON.parse(tableSection.dataset.allParams || '[]');
        this.allHeaders = JSON.parse(tableSection.dataset.allHeaders || '[]');
        this.allActions = JSON.parse(tableSection.dataset.allActions || '[]');
        this.allLinks = JSON.parse(tableSection.dataset.allLinks || '[]');
        this.allEndpoints = JSON.parse(tableSection.dataset.allEndpoints || '[]');

        this.searchValue = this?.searchInput?.value || '';
        this.currentColumn = '';
        this.currentOrder = '';
        this.delay = Math.max(1000, parseInt(tableSection.dataset.delay));
        this.prevData = {};

        this.page = 1;
        this.records = 5;
        this.totalPages = 1;

        this.init();
    }

    init() {
        this.fetchData();
        this.searchInput?.addEventListener('input', () => this.handleSearchChange());
        this.resetBtn?.addEventListener('click', () => this.handleResetFilters());
        this.sortableColumns?.forEach(column => {
            column.addEventListener('click', () => this.handleSortingChange(column));
            column.addEventListener('keypress', (event) => {
                if (event.key === 'Enter' || event.key === ' ') {
                    this.handleSortingChange(column);
                }
            });
        });

        this.addPaginationControls();
        this.addRecordsDropdownEvent();

        setInterval(() => {
            const tbody = document.querySelector('tbody');
            if (tbody && tbody.innerHTML.trim() === "") {
                this.renderEmptyTable();
            }
        }, 250);

        window.addEventListener('table-refresh', () => {
            this.fetchData();
        });

        setInterval(() => {
            this.fetchData();
        }, this.delay);
    }

    fetchData() {
        this.renderResetButton();
        const searchTermEncoded = encodeURIComponent(this.searchValue);
        const url = `/api/${this.apiEndpoint}/?sorteer_op=${this.currentColumn}&volgorde=${this.currentOrder}&zoekterm=${searchTermEncoded}&pagina=${this.page}&aantal=${this.records}${this.params || ''}`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (!data.data || data.data.length === 0) {
                    this.prevData = {};
                    this.totalRecords.textContent = '0';
                    this.renderEmptyTable();
                    this.updatePagination();
                    return;
                }

                const dataJson = JSON.stringify(data);
                if (this.prevData !== dataJson) {
                    this.prevData = dataJson;
                    this.totalRecords.textContent = data.total_records;
                    this.renderTableRows(data.data);
                    this.updatePagination(data.total_pages, data.current_page);
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                this.renderErrorTable();
            });
    }

    renderTableRows(rows) {
        this.tableBody.innerHTML = rows.map(row => {
            return `
            <tr>
                ${this.columnKeys.map(column => `<td>${row[column]}</td>`).join('')}
                ${this.actions.length ? `<td class="text-nowrap text-end">${this.renderActionButtons(row)}</td>` : ''}
            </tr>
        `;
        }).join('');
    }

    renderActionButtons(row) {
        return this.actions.map(action => {
            if (action.key === 'aanmelding') {
                if (action.role === 'button') {
                    return `
                        <button 
                            class="btn ${action.class} action-btn" 
                            data-action="${action.label}" 
                            data-onderzoek_id="${row['onderzoek_id']}"
                            data-gebruiker_id="${row['gebruiker_id']}">
                            <i class="${action.icon}"></i> ${action.label}
                        </button>
                    `;
                }
            }

            if (action.role === 'button') {
                return `
                    <button 
                        class="btn ${action.class} action-btn" 
                        data-action="${action.label}" 
                        data-id="${row[action.key]}">
                        <i class="${action.icon}"></i> ${action.label}
                    </button>
                `;
            } else if (action.role === 'link') {
                return `
                    <a 
                        href="/${this.linkEndpoint}/${row[action.key]}" 
                        class="btn ${action.class} action-btn">
                        <i class="${action.icon}"></i> ${action.label}
                    </a>
                `;
            }
        }).join('');
    }

    renderEmptyTable() {
        this.tableBody.innerHTML = `
        <tr>
            <td class="text-center py-5" colspan="${this.colSpan}">
                <i class="fa-solid fa-folder-open pb-2" aria-hidden="true"></i>
                <p class="no-results-message" role="alert" >Geen passende ${this.placeholder} gevonden</p>
            </td>
        </tr>`;
    }

    renderErrorTable() {
        this.tableBody.innerHTML = `
            <tr>
                <td class="text-center py-5" colspan="${this.colSpan}">
                    <i class="fa-solid fa-exclamation-circle pb-2" aria-hidden="true"></i>
                    <p class="error-message" role="alert" >Er is iets fout gegaan bij het ophalen van de ${this.placeholder}</p>
                </td>
            </tr>`;
    }

    renderResetButton() {
        const isVisible = this?.searchValue || this?.currentColumn || this?.currentOrder;
        this?.resetBtn?.classList.toggle('d-none', !isVisible);
    }

    handleSortingChange(column) {
        this.currentColumn = column.dataset.column;
        this.currentOrder = column.dataset.order = column.dataset.order === 'asc' ? 'desc' : 'asc';
        this.fetchData();

        // reset all columns orders
        this.sortableColumns.forEach(column => {
            column.setAttribute('data-order', 'none');
            column.setAttribute('aria-sort', 'none');
        });

        // set order current column
        let ariaSort = this.currentOrder === 'asc' ? 'ascending' : 'descending';
        column.setAttribute('aria-sort', ariaSort);
        column.setAttribute('data-order', this.currentOrder);
    }

    handleSearchChange() {
        this.searchValue = this.searchInput.value;
        this.fetchData();
    }

    handleResetFilters() {
        this.searchInput.value = '';
        this.searchValue = '';
        this.currentColumn = '';
        this.currentOrder = '';
        this.sortableColumns.forEach(column => {
            column.setAttribute('data-order', 'none');
            column.setAttribute('aria-sort', 'none');
        });
        this.fetchData();
    }

    getColumnKeys() {
        return Array.from(this.tableHeader.querySelectorAll('[data-column]')).map(column => column.dataset.column);
    }

    addPaginationControls() {
        const prevButton = document.querySelector('.prev-page');
        const nextButton = document.querySelector('.next-page');

        nextButton.addEventListener('click', () => {
            if (this.page < this.totalPages) {
                this.page++;
                this.fetchData();
            }
        });

        prevButton.addEventListener('click', () => {
            if (this.page > 1) {
                this.page--;
                this.fetchData();
            }
        });
    }

    updatePagination(totalPages = 1, currentPage = 1) {
        const paginationContainer = document.querySelector(".pagination");
        this.totalPages = totalPages;
        this.page = currentPage;

        totalPages === 1 ? paginationContainer.classList.add("d-none") : paginationContainer.classList.remove("d-none");

        document.getElementById('current-page').textContent = this.page;
        document.getElementById('total-pages').textContent = this.totalPages;

        const prevButton = document.querySelector('.prev-page');
        const nextButton = document.querySelector('.next-page');

        prevButton.disabled = this.page <= 1;
        nextButton.disabled = this.page >= this.totalPages;

        this.renderPaginationNumbers();

    }

    renderPaginationNumbers() {
        const container = document.querySelector(".pagination-numbers");
        container.innerHTML = "";

        let startPage = this.page - 2;
        let endPage = this.page + 2;

        if (startPage < 1) {
            startPage = 1;
            endPage = Math.min(5, this.totalPages);
        }

        if (endPage > this.totalPages) {
            endPage = this.totalPages;
            startPage = Math.max(1, this.totalPages - 4);
        }

        if (startPage > 1) {
            let firstPageButton = document.createElement("button");
            firstPageButton.textContent = "1";
            firstPageButton.setAttribute('aria-label', "Ga naar eerste pagina");
            firstPageButton.title = "Ga naar eerste pagina";

            firstPageButton.addEventListener('click', () => {
                this.page = 1;
                this.fetchData();
            });

            container.appendChild(firstPageButton);

            if (startPage > 2) {
                let dots = document.createElement("span");
                dots.textContent = "...";
                dots.classList.add("pagination-dots");
                container.appendChild(dots);
            }
        }

        for (let i = startPage; i <= endPage; i++) {
            let button = document.createElement("button");
            button.textContent = i;
            button.setAttribute('aria-label', `Ga naar pagina ${i}`);
            button.title = `Ga naar pagina ${i}`;

            if (i === this.page) {
                button.classList.add('active');
            }

            button.addEventListener('click', () => {
                this.page = i;
                this.fetchData();
            });

            container.appendChild(button);
        }

        if (endPage < this.totalPages) {
            if (endPage < this.totalPages - 1) {
                let dots = document.createElement("span");
                dots.textContent = "...";
                dots.classList.add("pagination-dots");
                container.appendChild(dots);
            }

            let lastPageButton = document.createElement("button");
            lastPageButton.textContent = this.totalPages;
            lastPageButton.setAttribute('aria-label', "Ga naar laatste pagina");
            lastPageButton.title = "Ga naar laatste pagina";

            lastPageButton.addEventListener('click', () => {
                this.page = this.totalPages;
                this.fetchData();
            });

            container.appendChild(lastPageButton);
        }
    }


    addRecordsDropdownEvent() {
        const dropdown = document.querySelector('.records-per-page');
        if (dropdown) {
            dropdown.addEventListener('change', (e) => {
                this.records = e.target.value;
                this.page = 1;
                this.fetchData();
            });
        }
    }

    updateTableHeaders(headers, has_action) {
        let theadContent = `<tr class="text-uppercase" aria-live="polite">`;

        headers.forEach(header => {
            if (header.sortable) {
                theadContent += `
                    <th scope="col" class="p-3 text-muted text-nowrap sortable" tabindex="0"
                        aria-label="Sorteer op ${header.label}" aria-sort="none" data-order="none"
                        data-column="${header.key}">
                        ${header.label}
                        <i class="fa-solid fa-sort-up ps-2 d-none"></i>
                        <i class="fa-solid fa-sort-down ps-2 d-none"></i>
                        <i class="fa-solid fa-sort ps-2 d-none"></i>
                    </th>
                `;
            } else {
                theadContent += `
                    <th scope="col" class="p-3 text-muted text-nowrap" data-column="${header.key}">
                        ${header.label}
                    </th>
                `;
            }
        });

        if (has_action) {
            theadContent += `
                <th scope="col" class="p-3 text-muted text-nowrap text-end">Acties</th>
            `;
        }

        theadContent += `</tr>`;
        return theadContent;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const tableSection = document.querySelector('.table-section');
    if (tableSection) {
        const tableInstance = new Table(tableSection);

        document.querySelectorAll('.title').forEach(title => {
            title.addEventListener('click', () => {
                if (title.classList.contains('active')) {
                    return;
                }

                document.querySelector('.title.active')?.setAttribute('aria-selected', 'false');
                document.querySelector('.title.active')?.classList.remove('active');
                title.classList.add('active');
                title.setAttribute('aria-selected', 'true');

                // Update table headers
                const ths = tableInstance.tableHeader.querySelectorAll('th');
                const th = Array.from(ths).find(th => th.innerHTML.trim() === 'Acties');
                tableInstance.tableHeader.innerHTML = '';
                newHeaders = tableInstance.allHeaders[title.innerHTML]
                tableInstance.tableHeader.innerHTML = tableInstance.updateTableHeaders(newHeaders, th);

                // Update instance values
                // Columnkeys
                tableInstance.columnKeys = tableInstance.getColumnKeys();
                // Actions
                tableInstance.actions = tableInstance.allActions[title.innerHTML]
                // Columnspan
                tableInstance.colSpan = tableInstance.columnKeys.length + (tableInstance.actions.length || 0);
                // Sort
                tableInstance.sortableColumns = tableSection.querySelectorAll('.sortable');
                tableInstance.sortableColumns?.forEach(column => {
                    column.addEventListener('click', () => tableInstance.handleSortingChange(column));
                    column.addEventListener('keypress', (event) => {
                        if (event.key === 'Enter' || event.key === ' ') {
                            tableInstance.handleSortingChange(column);
                        }
                    });
                });
                // Link
                tableInstance.linkEndpoint = tableInstance.allLinks[title.innerHTML]
                // Endpoint
                tableInstance.apiEndpoint = tableInstance.allEndpoints[title.innerHTML]
                // Params
                tableInstance.params = tableInstance.allParams[title.innerHTML]
                // Placeholder
                tableInstance.placeholder = tableInstance.allPlaceholders[title.innerHTML]
                // Search;
                tableInstance.searchValue = '';
                const searchInput = document.querySelector('.search-input');
                if (searchInput) {
                    searchInput.placeholder = `Zoek ${tableInstance.allPlaceholders[title.innerHTML]}...`;
                    searchInput.id = `search-input-${tableInstance.allIds[title.innerHTML]}`;
                    searchInput.value = '';
                }
                // Pagination
                tableInstance.page = 1;
                tableInstance.records = 5
                document.querySelector('.records-per-page').value = '5';
                // Sort
                tableInstance.currentColumn = '';
                tableInstance.currentOrder = '';

                tableInstance.fetchData();
            });

            title.addEventListener('keydown', (event) => {
                if (event.key === "Enter" || event.key === " ") {
                    title.click();
                }
            });
        });
    }
});