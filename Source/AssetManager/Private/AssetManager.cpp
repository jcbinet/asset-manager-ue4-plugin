// Copyright Epic Games, Inc. All Rights Reserved.

#include "AssetManager.h"
#include "AssetManagerStyle.h"
#include "AssetManagerCommands.h"
#include "Misc/MessageDialog.h"
#include "ToolMenus.h"

static const FName AssetManagerTabName("AssetManager");

#define LOCTEXT_NAMESPACE "FAssetManagerModule"

void FAssetManagerModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
	
	FAssetManagerStyle::Initialize();
	FAssetManagerStyle::ReloadTextures();

	FAssetManagerCommands::Register();
	
	PluginCommands = MakeShareable(new FUICommandList);

	PluginCommands->MapAction(
		FAssetManagerCommands::Get().PluginAction,
		FExecuteAction::CreateRaw(this, &FAssetManagerModule::PluginButtonClicked),
		FCanExecuteAction());

	UToolMenus::RegisterStartupCallback(FSimpleMulticastDelegate::FDelegate::CreateRaw(this, &FAssetManagerModule::RegisterMenus));
}

void FAssetManagerModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.

	UToolMenus::UnRegisterStartupCallback(this);

	UToolMenus::UnregisterOwner(this);

	FAssetManagerStyle::Shutdown();

	FAssetManagerCommands::Unregister();
}

void FAssetManagerModule::PluginButtonClicked()
{
	FText DialogText = FText::Format(
		LOCTEXT("PluginButtonDialogText", "Asset Manager - Version {0} "),
		FText::FromString(TEXT("0.1.0"))
	);
	FMessageDialog::Open(EAppMsgType::Ok, DialogText);
}

void FAssetManagerModule::RegisterMenus()
{
	// Owner will be used for cleanup in call to UToolMenus::UnregisterOwner
	FToolMenuOwnerScoped OwnerScoped(this);

	{
		UToolMenu* Menu = UToolMenus::Get()->ExtendMenu("LevelEditor.MainMenu.Window");
		{
			FToolMenuSection& Section = Menu->FindOrAddSection("WindowLayout");
			Section.AddMenuEntryWithCommandList(FAssetManagerCommands::Get().PluginAction, PluginCommands);
		}
	}

	{
		UToolMenu* ToolbarMenu = UToolMenus::Get()->ExtendMenu("LevelEditor.LevelEditorToolBar");
		{
			FToolMenuSection& Section = ToolbarMenu->FindOrAddSection("Settings");
			{
				FToolMenuEntry& Entry = Section.AddEntry(FToolMenuEntry::InitToolBarButton(FAssetManagerCommands::Get().PluginAction));
				Entry.SetCommandList(PluginCommands);
			}
		}
	}
}

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FAssetManagerModule, AssetManager)