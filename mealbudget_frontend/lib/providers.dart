

import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'data/api_client.dart';
import 'data/mealbudget_api.dart';
import 'core/models.dart';

final apiClientProvider = Provider<ApiClient>((ref) {
  return ApiClient();
});

final mealBudgetApiProvider = Provider<MealBudgetApi>((ref) {
  return MealBudgetApi();
});

final planResultProvider = StateProvider<PlanResponse?>((ref) => null);