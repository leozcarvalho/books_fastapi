<template>
<div>
  <div class="container">
    <div class="row mb-5">
        <div class="col-md-4">
            <h1>Usuários</h1>
        </div>
        <div class="col-md-3 offset-2">
          <b-form-select v-model="user" :options="users"></b-form-select>
        </div>
        <div class="col-md-1" v-if = "user">
          <b-button variant="danger"
          size = "sm"
          @click = "delUser"
          >Excluir</b-button>
        </div>
    </div>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.user-modal
        >Add Usuário</button>
        <br><br>
        <Alert ref= "Alert"></Alert>
        <b-modal
            id="user-modal"
            ref="user-modal"
            title="Novo Usuário"
            @hidden="clearForm"
            @ok="addUser"
            >
            <form ref="form">
                <b-form-group
                label="Name"
                label-for="name-input"
                invalid-feedback="Nome é obrigatório"
                >
                <b-form-input
                    id="name-input"
                    v-model="user_form.name"
                    required
                ></b-form-input>
                </b-form-group>
                <b-form-group
                label="E-mail"
                label-for="email-input"
                invalid-feedback="E-mail é obrigatório"
                >
                <b-form-input
                    id="email-input"
                    v-model="user_form.email"
                    required
                ></b-form-input>
                </b-form-group>
            </form>
        </b-modal>
    <div class="row">
        <div class="col-md-10">
            <hr><br><br>
        </div>
    </div>
  </div>
  <div v-show = "user">
    <Books ref = "Books" :userId = "parseInt(userId, 10)"></Books>
  </div>
</div>
</template>

<script>

import axios from 'axios';
import Books from './Books.vue';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      users: null,
      user: null,
      userId: null,
      user_form: {
        name: null,
        email: null,
      },
    };
  },
  components: {
    Books,
    Alert,
  },

  created() {
    this.getUsers();
  },

  methods: {
    getUsers() {
      const path = 'http://localhost:8000/users';
      axios.get(path)
        .then((res) => {
          this.users = res.data.users;
          const users = this.users.map((item) => `${item.id} - ${item.name}`);
          this.users = users;
          this.clearForm();
        })
        .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        });
    },
    clearForm() {
      this.user_form.name = null;
      this.user_form.email = null;
    },
    addUser() {
      const path = 'http://localhost:8000/user/register';
      const payload = {
        user: {
          name: this.user_form.name,
          email: this.user_form.email,
        },
      };
      axios.post(path, payload)
        .then(() => {
          this.$refs.Alert.showAlert('Usuário adicionado com sucesso', 'success');
          this.getUsers();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    delUser() {
      const path = `http://localhost:8000/user/delete/${this.userId}`;
      axios.delete(path)
        .then(() => {
          this.$refs.Alert.showAlert('Usuário Removido!', 'danger');
          this.getUsers();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getUsers();
        });
    },
  },
  watch: {
    user() {
      [this.userId] = this.user.split('-');
      this.$refs.Books.ownerUser = this.userId;
      this.$refs.Books.getBooks();
    },
  },
};
</script>
