new Vue({
    el: '#app',
    delimiters: ['{$', '$}'],
    data: {
        vplataforma: '',
        vusuario: '',
        vcontrasena: '',
        vfecha_creacion: '',
        vclave_secreta: '',
        vlista_credenciales: []
    },
    watch: {
        vcliente: function (val) {
            // this.BuscarCompras(val);
        }
    },
    methods: {
        // GetCookie: function (name) {
        //     let cookieValue = null;
        //     if (document.cookie && document.cookie !== '') {
        //         const cookies = document.cookie.split(';');
        //         for (let i = 0; i < cookies.length; i++) {
        //             const cookie = cookies[i].trim();
        //             // Does this cookie string begin with the name we want?
        //             if (cookie.substring(0, name.length + 1) === (name + '=')) {
        //                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        //                 break;
        //             }
        //         }
        //     }
        //     return cookieValue;
        // },
        BuscarCompras: function () {
            var self = this;
            axios.get('/api/credenciales/list')
                .then(function (response) {
                    self.vlista_credenciales = response.data
                })
                .catch(function (error) {
                    console.log(error);
                })
        },
        CambiarEstado: function (estado) {
            axios.put('https://pm-project-api-rest.herokuapp.com/compra/update/' + this.vid_compra + '/' + estado.target.value)
                .then(function (response) {
                })
                .catch(function (error) {
                    console.log(error);
                })
            this.vid_compra = 0
        },
        CredencialCreate: function () {
            const fecha_actual = new Date
            var data_credencial = {
                'plataforma': this.vplataforma,
                'usuario': this.vusuario,
                'contrasena': this.vcontrasena,
                'fecha_creacion': fecha_actual,
            }
            axios.post('/api/credenciales/create', data_credencial)
                .then(function (response) {
                    self.vlista_credenciales = response.data
                    console.log(response)
                })
                .catch(function (error) {
                    console.log(error);
                })
            this.BuscarCompras()
        }
    },
    mounted() {
        this.BuscarCompras("")
    }
});