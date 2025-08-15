describe('Kanban E2E Test', () => {
  it('debe crear una tarea, moverla a En Progreso y persistir al recargar', () => {
    // Visitar la aplicación
    cy.visit('/');

    // Crear una nueva tarea
    const taskText = 'Tarea de prueba';
    cy.get('[data-testid="add-task-btn"]').click();
    cy.get('[data-testid="task-input"]').type(taskText);
    cy.get('[data-testid="create-task-submit"]').click();

    // Verificar que la tarjeta aparece en la columna Por Hacer
    cy.get('[data-testid="column-por-hacer"]')
      .find('[data-testid^="task-card-"]')
      .should('contain.text', taskText);

    // Obtener el ID de la tarea recién creada (asumiendo que el texto es único)
    let taskId;
    cy.get('[data-testid="column-por-hacer"]')
      .find('[data-testid^="task-card-"]')
      .filter(`:contains("${taskText}")`)
      .then($el => {
        const id = $el.attr('data-testid').replace('task-card-', '');
        taskId = id;
      });

    // Arrastrar la tarjeta a En Progreso
    cy.get(`[data-testid="task-card-${taskId}"]`).trigger('mousedown', { which: 1 });
    cy.get('[data-testid="column-en-progreso"]').trigger('mousemove').trigger('mouseup');

    // Verificar que la tarjeta se movió
    cy.get('[data-testid="column-en-progreso"]')
      .find(`[data-testid="task-card-${taskId}"]`)
      .should('exist');

    // Recargar la página y verificar persistencia
    cy.reload();

    // La tarea debe seguir estando en En Progreso después de recargar
    cy.get('[data-testid="column-en-progreso"]')
      .find(`[data-testid="task-card-${taskId}"]`)
      .should('exist');
  });
});