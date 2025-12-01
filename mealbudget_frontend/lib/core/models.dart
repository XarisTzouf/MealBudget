
// lib/core/models.dart

class MealRead {
  final int id;
  final String name;
  final String category; 
  final double cost;
  final double kcal;
  final double protein;
  final double fat;
  final double carbs;

  MealRead({
    required this.id,
    required this.name,
    required this.category,
    required this.cost,
    required this.kcal,
    required this.protein,
    required this.fat,
    required this.carbs,
  });

  factory MealRead.fromJson(Map<String, dynamic> json) {
    return MealRead(
      id: json['id'],
      name: json['name'],
      category: json['category'] ?? 'main', // Default τιμή αν δεν υπάρχει
      cost: (json['cost'] as num).toDouble(),
      kcal: (json['kcal'] as num).toDouble(),
      protein: (json['protein'] as num).toDouble(),
      fat: (json['fat'] as num).toDouble(),
      carbs: (json['carbs'] as num).toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'category': category,
      'cost': cost,
      'kcal': kcal,
      'protein': protein,
      'fat': fat,
      'carbs': carbs,
    };
  }
}

class PlanCreate {
  final String title;
  final double budget;
  final List<int> mealIds;

  PlanCreate({
    required this.title,
    required this.budget,
    required this.mealIds,
  });

  Map<String, dynamic> toJson() {
    return {
      'title': title,
      'budget': budget,
      'meal_ids': mealIds,
    };
  }
}

class PlanRead {
  final int id;
  final String title;
  final double budget;
  final List<MealRead> meals;

  PlanRead({
    required this.id,
    required this.title,
    required this.budget,
    required this.meals,
  });

  factory PlanRead.fromJson(Map<String, dynamic> json) {
    return PlanRead(
      id: json['id'],
      title: json['title'],
      budget: (json['budget'] as num).toDouble(),
      meals: (json['meals'] as List)
          .map((m) => MealRead.fromJson(m))
          .toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'budget': budget,
      'meals': meals.map((m) => m.toJson()).toList(),
    };
  }
}

class PlanItemCandidate {
  final int mealId;
  final String name;
  final String category; 
  final double cost;
  final double kcal;
  final double protein;
  final double fat;
  final double carbs;

  PlanItemCandidate({
    required this.mealId,
    required this.name,
    required this.category, 
    required this.cost,
    required this.kcal,
    required this.protein,
    required this.fat,
    required this.carbs,
  });

  Map<String, dynamic> toJson() {
    return {
      'meal_id': mealId,
      'name': name,
      'category': category, 
      'cost': cost,
      'kcal': kcal,
      'protein': protein,
      'fat': fat,
      'carbs': carbs,
    };
  }

  factory PlanItemCandidate.fromJson(Map<String, dynamic> json) {
    return PlanItemCandidate(
      mealId: json['meal_id'],
      name: json['name'],
      category: json['category'] ?? 'main',
      cost: (json['cost'] as num).toDouble(),
      kcal: (json['kcal'] as num).toDouble(),
      protein: (json['protein'] as num).toDouble(),
      fat: (json['fat'] as num).toDouble(),
      carbs: (json['carbs'] as num).toDouble(),
    );
  }
}

class PlanRow {
  final int mealId;
  final String name;
  final int qty;
  final double cost;
  final double kcal;
  final double protein;
  final double fat;
  final double carbs;

  PlanRow({
    required this.mealId,
    required this.name,
    required this.qty,
    required this.cost,
    required this.kcal,
    required this.protein,
    required this.fat,
    required this.carbs,
  });

  factory PlanRow.fromJson(Map<String, dynamic> json) {
    return PlanRow(
      mealId: json['meal_id'],
      name: json['name'],
      qty: json['qty'],
      cost: (json['cost'] as num).toDouble(),
      kcal: (json['kcal'] as num).toDouble(),
      protein: (json['protein'] as num).toDouble(),
      fat: (json['fat'] as num).toDouble(),
      carbs: (json['carbs'] as num).toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'meal_id': mealId,
      'name': name,
      'qty': qty,
      'cost': cost,
      'kcal': kcal,
      'protein': protein,
      'fat': fat,
      'carbs': carbs,
    };
  }
}

class PlanRequest {
  final String title;
  final double budget;
  final List<PlanItemCandidate> candidates;
  final double? kcalTarget;

  PlanRequest({
    required this.title,
    required this.budget,
    required this.candidates,
    this.kcalTarget,
  });

  Map<String, dynamic> toJson() {
    return {
      'title': title,
      'budget': budget,
      'candidates': candidates.map((c) => c.toJson()).toList(),
      'kcal_target': kcalTarget,
    };
  }
}

class PlanResponse {
  final String title;
  final List<PlanRow> rows;
  final double totalCost;
  final double totalKcal;
  final double totalProtein;
  final double totalFat;
  final double totalCarbs;

  PlanResponse({
    required this.title,
    required this.rows,
    required this.totalCost,
    required this.totalKcal,
    required this.totalProtein,
    required this.totalFat,
    required this.totalCarbs,
  });

  factory PlanResponse.fromJson(Map<String, dynamic> json) {
    return PlanResponse(
      title: json['title'],
      rows: (json['rows'] as List)
          .map((r) => PlanRow.fromJson(r))
          .toList(),
      totalCost: (json['total_cost'] as num).toDouble(),
      totalKcal: (json['total_kcal'] as num).toDouble(),
      totalProtein: (json['total_protein'] as num).toDouble(),
      totalFat: (json['total_fat'] as num).toDouble(),
      totalCarbs: (json['total_carbs'] as num).toDouble(),
    );
  }
}