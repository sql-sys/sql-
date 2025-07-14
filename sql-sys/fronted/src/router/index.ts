import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
import LoginView from '../views/LoginView.vue'
import HomeView from '../views/HomeView.vue'
import AdminSemesterView from '../views/AdminSemesterView.vue'
import AdminTeacherView from '../views/AdminTeacherView.vue'
import StudentHomeView from '../views/StudentHomeView.vue'
import TeacherHomeView from '../views/TeacherHomeView.vue'
import TeacherDashboardView from '../views/TeacherDashboardView.vue'
import TeacherMatrixView from '../views/TeacherMatrixView.vue'
import TeacherScoreCalculateView from '../views/TeacherScoreCalculateView.vue'
import TeacherDatabaseSchemaView from '../views/TeacherDatabaseSchemaView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/admin/semester',
      name: 'admin-semester',
      component: AdminSemesterView,
      meta: { requiresAuth: true }
    },
    {
      path: '/admin/teacher',
      name: 'admin-teacher',
      component: AdminTeacherView,
      meta: { requiresAuth: true }
    },
    {
      path: '/student/home',
      name: 'student-home',
      component: StudentHomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/student/task',
      name: 'student-task',
      component: () => import('../views/StudentTaskView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/student/dashboard',
      name: 'student-dashboard',
      component: () => import('../views/StudentDashboardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/teacher/home',
      name: 'teacher-home',
      component: TeacherHomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/teacher/dashboard',
      name: 'teacher-dashboard',
      component: TeacherDashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/teacher/dashboard/matrix/:semester_id',
      name: 'teacher-matrix',
      component: TeacherMatrixView,
      meta: { requiresAuth: true }
    },
    {
      path: '/teacher/dashboard/score-calculate/:semester_id',
      name: 'teacher-score-calculate',
      component: TeacherScoreCalculateView,
      meta: { requiresAuth: true }
    },
    // 教师其他页面路由
    {
      path: '/teacher/database-schema',
      name: 'teacher-database-schema',
      component: TeacherDatabaseSchemaView,
      meta: { requiresAuth: true }
    },
    {
      path: '/teacher/problem',
      name: 'teacher-problem',
      component: () => import('../views/TeacherProblemView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/teacher/student-info',
      name: 'teacher-student-info',
      component: () => import('../views/TeacherStudentInfoView.vue'),
      meta: { requiresAuth: true }
    },
    // {
    //   path: '/teacher/info',
    //   name: 'teacher-info',
    //   component: () => import('../views/TeacherInfoView.vue'),
    //   meta: { requiresAuth: true }
    // },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  // 如果访问的是登录页面，直接放行
  if (to.path === '/login') {
    next()
    return
  }

  // 如果路由需要认证但没有token，重定向到登录页
  if (to.meta.requiresAuth && !token) {
    ElMessage.warning('请先登录')
    next('/login')
    return
  }

  next()
})

export default router
