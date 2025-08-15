describe('Prueba E2E de la aplicación Kanban', () => {
  it('añade, edita, mueve y elimina una tarea correctamente', () => {
    // Abrir la página principal
    cy.visit('/');

    // Añadir una nueva tarea en "Por Hacer"
    cy.get('[data-testid="add-task-button"]').click();
    cy.get('[data-testid="task-input"]').type('Nueva Tarea{enter}');

    // Verificar que la tarjeta aparece en la columna Por Hacer
    cy.get('[data-testid="column-todo"]')
      .find('[data-testid="task-card"]')
      .should('contain.text', 'Nueva Tarea');

    // Editar el texto de la tarea
    cy.get('[data-testid="column-todo"]')
      .find('[data-testid="task-card"]')
      .click(); // abre modo edición
    cy.get('[data-testid="edit-task-input"]').clear().type('Tarea Editada{enter}');

    // Verificar que el texto se actualizó
    cy.get('[data-testid="column-todo"]')
      .find('[data-testid="task-card"]')
      .should('contain.text', 'Tarea Editada');

    // Mover la tarjeta a "En Progreso" (drag and drop simulación)
    cy.get('[data-testid="column-todo"]')
      .find('[data-testid="task-card"]')
      .trigger('mousedown');
    cy.get('[data-testid="column-inprogress"]').trigger('mousemove').trigger('mouseup');

    // Verificar que la tarjeta ahora está en En Progreso
    cy.get('[data-testid="column-inprogress"]')
      .find('[data-testid="task-card"]')
      .should('contain.text', 'Tarea Editada');

    // Eliminar la tarea
    cy.get('[data-testid="column-inprogress"]')
      .find('[data-testid="task-card"]')
      .within(() => {
        cy.get('[data-testid="delete-task"]').click();
      });

    // Verificar que la tarjeta ya no existe en ninguna columna
    cy.get('[data-testid="column-todo"]')
      .find('[data-testid="task-card"]')
      .should('not.exist');
    cy.get('[data-testid="column-inprogress"]')
      .find('[data-testid="task-card"]')
      .should('not.exist');
    cy.get('[data-testid="column-done"]')
      .find('[data-testid="task-card"]')
      .should('not.exist');
  });
});