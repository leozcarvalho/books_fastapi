<template>
  <div class="container">
    <div class="row">
      <div class="col-md-10">
        <h1>Livros</h1>
        <hr><br><br>
        <Alert ref= "Alert"></Alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.book-modal
        @click="onShowModalInsert">Add Livro</button>
        <br><br>
        <b-spinner v-if = "loading"
        class = "offset-5 mt-3" style="width: 5rem; height: 5rem;"
        label="Large Spinner"></b-spinner>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Título</th>
              <th scope="col">Autor</th>
              <th scope="col">Lido?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <h3 v-if = "books.length === 0" >
              Você não possui livros adicionados.</h3>
            <tr  v-for="(book, index) in books" :key="index">
              <td>{{ book.title }}</td>
              <td>{{ book.author }}</td>
              <td>
                <span v-if="book.read">Sim</span>
                <span v-else>Não</span>
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button
                          type="button"
                          class="btn btn-warning btn-sm"
                          v-b-modal.book-modal
                          @click="editBook(book, book.id)">
                      Alterar
                  </button>
                  <b-button type="button" class="btn btn-danger btn-sm"
                    @click="onShowDelete(book.id)">
                      Excluir
                  </b-button>
                </div>
              </td>
            </tr>
          <!--------------------Modal Excluir ------------------------------>
            <b-modal id="modal-del" size="sm"
                title="Atenção"
                header-bg-variant="warning"
            >
                Deseja realmente excluir este Livro?
                <template #modal-footer="{ ok, cancel }">
                    <b-button size="sm" variant="danger" @click="removeBook(bookId)">
                        Excluir
                    </b-button>
                    <b-button size="sm" variant="primary" @click="cancel()">
                        Cancelar
                    </b-button>
                </template>
            </b-modal>
          <!------------------------------------------------------------------>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="BookModal"
            id="book-modal"
            :title = "tituloModal"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-title-edit-group"
                    label="Título:"
                    label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="BookForm.title"
                        required
                        placeholder="Insira o título">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-author-edit-group"
                      label="Autor:"
                      label-for="form-author-edit-input">
            <b-form-input id="form-author-edit-input"
                          type="text"
                          v-model="BookForm.author"
                          required
                          placeholder="Insira o autor">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-read-edit-group">
            <b-form-checkbox v-model="BookForm.read"
            value="true">Lido?</b-form-checkbox>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">{{ botao }}</b-button>
          <b-button type="reset" variant="danger">Cancelar</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>

import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      books: [],
      BookForm: {
        title: '',
        author: '',
        read: false,
      },
      ownerUser: null,
      message: '',
      bookId: '',
      showMessage: false,
      dismissCountDown: 0,
      tituloModal: '',
      variant: '',
      botao: '',
      loading: false,
    };
  },
  components: {
    Alert,
  },
  methods: {
    onShowDelete(bookId) {
      this.bookId = bookId;
      this.$bvModal.show('modal-del');
    },
    onShowModalInsert() {
      this.tituloModal = 'Adicionar Livro';
      this.botao = 'Adicionar';
      this.initForm();
    },
    showAlert(message, variant) {
      this.dismissCountDown = 5;
      this.variant = variant;
      this.message = message;
    },
    getBooks() {
      const path = `http://localhost:8000/books/${this.ownerUser}`;
      this.loading = true;
      axios.get(path)
        .then((res) => {
          this.books = res.data.books;
          this.loading = false;
        })
        .catch((error) => {
          this.books = [];
          this.loading = false;
          this.$refs.Alert.showAlert('Este Usuário Ainda nao possui livros cadastrados!', 'danger');
          console.error(error);
        });
    },
    addBook(payload) {
      const path = `http://localhost:8000/book/save/${this.ownerUser}`;
      axios.post(path, payload)
        .then(() => {
          this.getBooks();
          this.$refs.Alert.showAlert('Livro Adicionado!', 'info');
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getBooks();
        });
    },
    updateBook(payload, bookID) {
      const path = `http://localhost:8000/book/update/${bookID}`;
      axios.put(path, payload)
        .then(() => {
          this.getBooks();
          this.$refs.Alert.showAlert('Livro Atualizado!', 'primary');
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
    initForm() {
      this.BookForm.title = '';
      this.BookForm.author = '';
      this.BookForm.read = false;
      this.bookId = null;
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.BookModal.hide();
      let read = false;
      if (this.BookForm.read) {
        read = true;
      }
      const payload = {
        book:
            {
              title: this.BookForm.title,
              author: this.BookForm.author,
              read, // property shorthand
            },
      };
      if (this.tituloModal === 'Adicionar Livro') {
        payload.owner_user = this.owner_user;
        this.addBook(payload);
      } else {
        this.updateBook(payload, this.bookId);
      }
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.BookModal.hide();
      this.initForm();
    },
    editBook(book, bookId) {
      this.tituloModal = 'Alterar';
      this.botao = 'Atualizar';
      this.BookForm = book;
      this.bookId = bookId;
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.BookModal.hide();
      this.initForm();
      this.getBooks(); // why?
    },
    removeBook(bookID) {
      const path = `http://localhost:8000/book/delete/${bookID}`;
      axios.delete(path)
        .then(() => {
          this.$bvModal.hide('modal-del');
          this.getBooks();
          this.$refs.Alert.showAlert('Livro Removido!', 'danger');
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
  },
};
</script>
