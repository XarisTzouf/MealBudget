import 'package:go_router/go_router.dart';

import '../features/home/home_page.dart';
import '../features/params/params_page.dart';
import '../features/results/results_page.dart';


final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomePage(),
    ),
    GoRoute(
      path: '/params',
      builder: (context, state) => const ParamsPage(),
    ),
    GoRoute(
      path: '/results',
      builder: (context, state) => const ResultsPage(),
    ),
  ],
);
