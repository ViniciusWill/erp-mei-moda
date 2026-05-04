import { onReady } from "./core/dom.js";
import { FormularioValidator } from "./ui/formulario-validator.js";
import { Toast } from "./ui/toast.js";

onReady(() => {
    FormularioValidator.inicializarTodos();
    Toast.exibirFlashMessages();
});
