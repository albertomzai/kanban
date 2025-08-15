describe('Prueba E2E de Kanban', () => {
  it('debe crear, editar, mover y eliminar una tarea correctamente', () => {
    // Visitar la página principal
    cy.visit('/');

    // Añadir una nueva tarea con contenido de prueba
    const taskContent = 'Tarea de prueba';
    cy.get('[data-testid="new-task-input"]').type(taskContent);
    cy.get('[data-testid="add-task-btn"]').click();

    // Verificar que la tarjeta aparece bajo "Por Hacer"
    cy.get('[data-testid="column-todo"]')
      .find('[data-testid^="task-card-"]')
      .should('contain.text', taskContent);

    // Cambiar el texto de la tarjeta y confirmar la actualización
    const updatedContent = 'Tarea actualizada';
    cy.get('[data-testid="column-todo"]')
      .find('[data-testid^="task-card-"]')
      .click(); // abrir modo edición
    cy.get('[data-testid="edit-task-input"]').clear().type(updatedContent);
    cy.get('[data-testid="save-edit-btn"]').click();
    cy.get('[data-testid="column-todo"]')
      .find('[data-testid^="task-card-"]')
      .should('contain.text', updatedContent);

    // Arrastrar la tarjeta a la columna "En Progreso" y verificar el cambio de estado
    const card = cy.get('[data-testid="column-todo"]').find('[data-testid^="task-card-"]');
    const targetColumn = cy.get('[data-testid="column-inprogress"]');

    // Simular drag-and-drop
    card.trigger('dragstart', { dataTransfer: new DataTransfer() });
    targetColumn.trigger('drop', { dataTransfer: new DataTransfer() });

    // Verificar que la tarjeta ya no está en "Por Hacer" y sí en "En Progreso"
    cy.get('[data-testid="column-todo"]').find('[data-testid^="task-card-"]').should('not.exist');
    cy.get('[data-testid="column-inprogress"]')
      .find('[data-testid^="task-card-"]')
      .should('contain.text', updatedContent);

    // Eliminar la tarjeta y asegurar que ya no se muestra en ninguna columna
    cy.get('[data-testid="column-inprogress"]').find('[data-testid^="task-card-"]').click(); // abrir opciones
    cy.get('[data-testid="delete-task-btn"]').click();
    cy.on('window:confirm', () => true); // confirmar eliminación si aparece

    // Comprobar que la tarjeta desaparece de todas las columnas
    cy.get('[data-testid^="column-"]').each(($col) => {
      cy.wrap($col).find('[data-testid^="task-card-"]').should('not.exist');
    });
  });
});