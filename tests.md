
# Scénario de tests

## 📌 Créer une fiche (status : DEFAULT) 
### test_create_fiche ✅

## Consulter les fiches (toutes)

## Consulter les fiches (status : DEFAULT)

## 📌 Modifier une fiche (status : DEFAULT) ✅

### test_cant_update_fiche_not_existing ✅
### test_update_fiche_lastname_only ✅
### test_update_fiche_firstname_only ✅
### test_update_fiche_telephone_only ✅
### test_update_fiche_email_only ✅
### test_update_fiche_address_only ✅
### test_update_fiche_origin_only ✅
### test_update_fiche_works_planned_only ✅
### test_update_fiche_both ✅


## 📌 Supprimer une fiche (status : DEFAULT)

### test_cant_delete_fiche_not_existing ✅
### test_delete_fiche ✅



### Champs Fiche contact (status : DEFAULT)
- firstname
- telephone
- email
- address

## 📌 Completer fiche contact (status : IN_PROGESS)

### test_cant_completion_fiche_status_default
### test_cant_completion_fiche_void
### test_completion_fiche


### test_config_service_load_config
    
### test_config_service_get_schema
    
### test_create_fiche_usecase_statut_default
    
### test_update_fiche_usecase_set_in_progress_when_required_fields_present
    
### test_completion_fiche_usecase_finalizes_fiche_with_valid_data
    
### test_fenetre_schema_requires_tirant_for_single_leaf_types
    
### test_fenetre_schema_allows_optional_tirant_for_other_window_types
    
### test_dynamic_form_endpoint_returns_correct_schema
